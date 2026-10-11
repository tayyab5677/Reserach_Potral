"""
app.py — Flask REST API for Research Opportunity Portal
=========================================================
Provides CRUD endpoints for managing research opportunities.
All data is stored in and retrieved from a MySQL database.
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from db import get_db_connection, DBError as Error
from validators import validate_opportunity

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS so the frontend (served from a different port) can access the API
CORS(app)


# ============================================================
# Helper: Convert a database row (tuple) to a dictionary
# ============================================================
def row_to_dict(row):
    """Convert a single database row to a dictionary."""
    deadline = row[8]
    if hasattr(deadline, 'strftime'):
        deadline_str = deadline.strftime('%Y-%m-%d')
    elif deadline:
        deadline_str = str(deadline)[:10]
    else:
        deadline_str = None

    return {
        'id': row[0],
        'title': row[1],
        'description': row[2],
        'research_area': row[3],
        'faculty_name': row[4],
        'department': row[5],
        'required_skills': row[6],
        'positions_available': row[7],
        'application_deadline': deadline_str,
        'status': row[9],
    }


# ============================================================
# GET / — Root API Health & Info Endpoint
# ============================================================
@app.route('/', methods=['GET'])
def index():
    """Welcome and health-check endpoint for the REST API."""
    return jsonify({
        'name': 'University Research Opportunity Portal API',
        'status': 'online',
        'endpoints': {
            'list_opportunities': '/api/opportunities',
            'create_opportunity': '/api/opportunities',
            'get_opportunity': '/api/opportunities/<id>',
            'update_opportunity': '/api/opportunities/<id>',
            'delete_opportunity': '/api/opportunities/<id>'
        },
        'frontend_url': 'http://localhost:8080'
    }), 200


# ============================================================
# POST /api/opportunities — Create a new opportunity
# ============================================================
@app.route('/api/opportunities', methods=['POST'])
def create_opportunity():
    """Create a new research opportunity."""
    # Parse JSON body
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Request body must be valid JSON'}), 400

    # Validate input
    errors = validate_opportunity(data, is_update=False)
    if errors:
        return jsonify({'error': ', '.join(errors)}), 400

    # Insert into database
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = """
            INSERT INTO opportunities
                (title, description, research_area, faculty_name, department,
                 required_skills, positions_available, application_deadline)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['title'].strip(),
            data['description'].strip(),
            data['research_area'].strip(),
            data['faculty_name'].strip(),
            data['department'].strip(),
            data['required_skills'].strip(),
            data['positions_available'],
            data['application_deadline'].strip(),
        )

        cursor.execute(sql, values)
        connection.commit()

        return jsonify({
            'message': 'Opportunity created successfully',
            'id': cursor.lastrowid
        }), 201

    except Error as e:
        print(f"[DB ERROR] {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# ============================================================
# GET /api/opportunities — List all opportunities
# ============================================================
@app.route('/api/opportunities', methods=['GET'])
def get_all_opportunities():
    """Retrieve all research opportunities."""
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, title, description, research_area, faculty_name,
                   department, required_skills, positions_available,
                   application_deadline, status
            FROM opportunities
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()
        opportunities = [row_to_dict(row) for row in rows]

        return jsonify(opportunities), 200

    except Error as e:
        print(f"[DB ERROR] {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# ============================================================
# GET /api/opportunities/<id> — Get one opportunity by ID
# ============================================================
@app.route('/api/opportunities/<int:opp_id>', methods=['GET'])
def get_opportunity(opp_id):
    """Retrieve a single research opportunity by its ID."""
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, title, description, research_area, faculty_name,
                   department, required_skills, positions_available,
                   application_deadline, status
            FROM opportunities
            WHERE id = %s
        """, (opp_id,))

        row = cursor.fetchone()

        if row is None:
            return jsonify({'error': f'Opportunity with id {opp_id} not found'}), 404

        return jsonify(row_to_dict(row)), 200

    except Error as e:
        print(f"[DB ERROR] {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# ============================================================
# PUT /api/opportunities/<id> — Update an opportunity
# ============================================================
@app.route('/api/opportunities/<int:opp_id>', methods=['PUT'])
def update_opportunity(opp_id):
    """Update an existing research opportunity (partial or full update)."""
    # Parse JSON body
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Request body must be valid JSON'}), 400

    # Check that at least one field is provided
    if not data:
        return jsonify({'error': 'No fields provided to update'}), 400

    # Validate input (partial update mode)
    errors = validate_opportunity(data, is_update=True)
    if errors:
        return jsonify({'error': ', '.join(errors)}), 400

    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # First, check if the opportunity exists
        cursor.execute("SELECT id FROM opportunities WHERE id = %s", (opp_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': f'Opportunity with id {opp_id} not found'}), 404

        # Build dynamic UPDATE query from provided fields
        updatable_fields = [
            'title', 'description', 'research_area', 'faculty_name',
            'department', 'required_skills', 'positions_available',
            'application_deadline', 'status'
        ]

        set_clauses = []
        values = []

        for field in updatable_fields:
            if field in data:
                set_clauses.append(f"{field} = %s")
                value = data[field]
                # Strip whitespace from string values
                if isinstance(value, str):
                    value = value.strip()
                values.append(value)

        if not set_clauses:
            return jsonify({'error': 'No valid fields provided to update'}), 400

        # Add the ID for the WHERE clause
        values.append(opp_id)

        sql = f"UPDATE opportunities SET {', '.join(set_clauses)} WHERE id = %s"
        cursor.execute(sql, tuple(values))
        connection.commit()

        return jsonify({'message': 'Opportunity updated successfully'}), 200

    except Error as e:
        print(f"[DB ERROR] {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# ============================================================
# DELETE /api/opportunities/<id> — Delete an opportunity
# ============================================================
@app.route('/api/opportunities/<int:opp_id>', methods=['DELETE'])
def delete_opportunity(opp_id):
    """Delete a research opportunity by its ID."""
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the opportunity exists
        cursor.execute("SELECT id FROM opportunities WHERE id = %s", (opp_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': f'Opportunity with id {opp_id} not found'}), 404

        # Delete the record
        cursor.execute("DELETE FROM opportunities WHERE id = %s", (opp_id,))
        connection.commit()

        return jsonify({'message': 'Opportunity deleted successfully'}), 200

    except Error as e:
        print(f"[DB ERROR] {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# ============================================================
# Global Error Handlers
# ============================================================
@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors for undefined routes."""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 errors for unsupported HTTP methods."""
    return jsonify({'error': 'Method not allowed'}), 405


@app.errorhandler(500)
def internal_error(e):
    """Handle unexpected 500 errors without leaking internals."""
    return jsonify({'error': 'An internal server error occurred'}), 500


# ============================================================
# Run the application
# ============================================================
if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    print(f"[OK] Research Opportunity Portal API running on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
