"""
db.py — Database Connection Helper (MySQL with SQLite Fallback)
===============================================================
Provides a reusable function to get a database connection.
Supports MySQL (via mysql-connector-python or PyMySQL) and automatically
falls back to an embedded SQLite database if MySQL server is not running
or DB_TYPE is configured as 'sqlite'.
"""

import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

# Determine DB provider
DB_TYPE = os.getenv('DB_TYPE', 'mysql').lower()

# Check for MySQL libraries
mysql_module = None
try:
    import mysql.connector
    mysql_module = 'mysql.connector'
except ImportError:
    try:
        import pymysql
        mysql_module = 'pymysql'
    except ImportError:
        mysql_module = None


class DBError(Exception):
    """Unified database error for backend API exception handling."""
    pass


# ---------------------------------------------------------------------------
# SQLite Compatibility Wrappers (to match MySQL interface)
# ---------------------------------------------------------------------------
class SQLiteCursorWrapper:
    """Wraps sqlite3.Cursor to support MySQL-style %s placeholders and properties."""
    def __init__(self, cursor):
        self._cursor = cursor
        self.lastrowid = None

    def execute(self, sql, params=None):
        # Convert MySQL %s placeholders to SQLite ? placeholders
        sql_adapted = sql.replace('%s', '?')
        try:
            if params is None:
                res = self._cursor.execute(sql_adapted)
            else:
                res = self._cursor.execute(sql_adapted, params)
            self.lastrowid = self._cursor.lastrowid
            return res
        except sqlite3.Error as e:
            raise DBError(str(e)) from e

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def close(self):
        try:
            self._cursor.close()
        except sqlite3.Error:
            pass


class SQLiteConnectionWrapper:
    """Wraps sqlite3.Connection to provide is_connected() and MySQL compatibility."""
    def __init__(self, conn):
        self._conn = conn
        self._closed = False

    def cursor(self):
        return SQLiteCursorWrapper(self._conn.cursor())

    def commit(self):
        try:
            self._conn.commit()
        except sqlite3.Error as e:
            raise DBError(str(e)) from e

    def rollback(self):
        try:
            self._conn.rollback()
        except sqlite3.Error as e:
            raise DBError(str(e)) from e

    def is_connected(self):
        return not self._closed

    def close(self):
        if not self._closed:
            self._closed = True
            self._conn.close()


def _get_sqlite_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'research_portal.sqlite')
    return db_path


def _init_sqlite_db(conn):
    """Initialize schema and seed initial sample opportunities if table is empty."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id                    INTEGER PRIMARY KEY AUTOINCREMENT,
            title                 VARCHAR(200) NOT NULL,
            description           TEXT NOT NULL,
            research_area         VARCHAR(100) NOT NULL,
            faculty_name          VARCHAR(100) NOT NULL,
            department            VARCHAR(100) NOT NULL,
            required_skills       VARCHAR(500) NOT NULL,
            positions_available   INTEGER NOT NULL CHECK (positions_available >= 0),
            application_deadline  TEXT NOT NULL,
            status                TEXT NOT NULL DEFAULT 'Open' CHECK (status IN ('Open', 'Closed')),
            created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at            DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM opportunities")
    count = cursor.fetchone()[0]
    if count == 0:
        seed_data = [
            (
                'AI Research Assistant — Urdu NLP',
                'Join our lab to work on Natural Language Processing models for Urdu text classification and sentiment analysis. You will help build datasets, train transformer models, and evaluate results on real-world social media data.',
                'Artificial Intelligence',
                'Dr. Ahmed Khan',
                'Computer Science',
                'Python, PyTorch, NLP basics, Linguistics',
                3,
                '2026-12-15',
                'Open'
            ),
            (
                'Cybersecurity Vulnerability Analysis',
                'Assist in identifying and documenting security vulnerabilities in IoT devices used in smart campus infrastructure. Hands-on penetration testing and report writing.',
                'Cybersecurity',
                'Dr. Fatima Noor',
                'Information Technology',
                'Networking, Linux, Wireshark, Ethical Hacking basics',
                2,
                '2026-11-30',
                'Open'
            ),
            (
                'Data Visualization for Climate Research',
                'Help build interactive dashboards to visualize 10 years of climate data from weather stations across Pakistan. The project involves data cleaning, statistical analysis, and D3.js visualization.',
                'Data Science',
                'Prof. Bilal Hussain',
                'Software Engineering',
                'JavaScript, D3.js, Python, Pandas, SQL',
                4,
                '2026-11-01',
                'Closed'
            ),
        ]
        cursor.executemany("""
            INSERT INTO opportunities
                (title, description, research_area, faculty_name, department,
                 required_skills, positions_available, application_deadline, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, seed_data)
        conn.commit()
    cursor.close()


def get_sqlite_connection():
    """Create and return a wrapped SQLite connection with auto-initialization."""
    db_path = _get_sqlite_db_path()
    raw_conn = sqlite3.connect(db_path)
    _init_sqlite_db(raw_conn)
    return SQLiteConnectionWrapper(raw_conn)


# ---------------------------------------------------------------------------
# Database Connection Factory
# ---------------------------------------------------------------------------
_mysql_available = None

def get_db_connection():
    """
    Create and return an active database connection.
    Attempts MySQL connection if configured. If MySQL is unavailable or DB_TYPE=sqlite,
    automatically falls back to SQLite.
    """
    global _mysql_available

    if DB_TYPE != 'sqlite' and mysql_module is not None and _mysql_available is not False:
        try:
            host = os.getenv('DB_HOST', 'localhost')
            port = int(os.getenv('DB_PORT', 3306))
            user = os.getenv('DB_USER', 'root')
            password = os.getenv('DB_PASSWORD', '')
            database = os.getenv('DB_NAME', 'research_portal')

            if mysql_module == 'mysql.connector':
                conn = mysql.connector.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    database=database,
                    connect_timeout=2
                )
                _mysql_available = True
                return conn
            elif mysql_module == 'pymysql':
                conn = pymysql.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    database=database,
                    connect_timeout=2
                )
                if not hasattr(conn, 'is_connected'):
                    conn.is_connected = lambda: bool(conn.open)
                _mysql_available = True
                return conn
        except Exception as e:
            _mysql_available = False
            print(f"[DB NOTICE] MySQL connection failed ({e}). Using embedded SQLite database.")

    # SQLite fallback
    return get_sqlite_connection()
