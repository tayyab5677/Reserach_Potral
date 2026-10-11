# University Research Opportunity Portal

> A centralized web application where faculty can post, manage, and share research opportunities, and students can browse them — all in one place.

**GitHub Repository:** `https://github.com/YOUR_USERNAME/research-opportunity-portal` _(replace with your actual link)_

---

## Features

- **Create** new research opportunities with full details
- **View** all opportunities in a responsive card grid
- **View** full details of any opportunity
- **Update** existing opportunities (edit any field)
- **Close** an opportunity (change status from Open → Closed)
- **Delete** an opportunity with confirmation dialog
- **Filter** by status (All / Open / Closed)
- **Validation** on both client and server side
- **Success & error alerts** for every action
- **Responsive** dark-themed UI with Bootstrap 5

---

## Tech Stack

| Layer    | Technology                         |
|----------|------------------------------------|
| Backend  | Python 3, Flask, flask-cors        |
| Database | MySQL 8 (mysql-connector-python)   |
| Frontend | HTML5, CSS3, JavaScript (vanilla)  |
| UI       | Bootstrap 5, Bootstrap Icons       |
| Font     | Google Fonts — Inter               |

---

## Folder Structure

```
research-opportunity-portal/
├── backend/
│   ├── app.py                 # Flask REST API (all endpoints)
│   ├── db.py                  # MySQL connection helper
│   ├── validators.py          # Server-side validation
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment variable template
├── frontend/
│   ├── index.html             # Single-page application
│   ├── css/
│   │   └── style.css          # Custom dark-theme styles
│   └── js/
│       └── app.js             # Frontend logic (fetch, DOM, forms)
├── database/
│   ├── schema.sql             # CREATE TABLE statement
│   └── seed.sql               # 3 sample research opportunities
├── postman/
│   └── Research_Opportunity_Portal.postman_collection.json
├── docs/
│   └── demo_script.md         # 60-second demo video script
├── README.md                  # This file
└── .gitignore                 # Ignores .env, __pycache__, etc.
```

---

## Prerequisites

Before starting, make sure you have:

- **Python 3.8+** installed ([python.org](https://www.python.org/downloads/))
- **MySQL 8.0+** installed and running ([dev.mysql.com](https://dev.mysql.com/downloads/))
- **pip** (Python package manager, comes with Python)
- A web browser (Chrome, Firefox, Edge)
- (Optional) **Postman** for API testing ([postman.com](https://www.postman.com/downloads/))

---

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/research-opportunity-portal.git
cd research-opportunity-portal
```

### Step 2: Create the MySQL Database and Tables

Open a MySQL client (MySQL Workbench, command line, etc.) and run:

```bash
mysql -u root -p < database/schema.sql
```

(Optional) Load sample data:

```bash
mysql -u root -p research_portal < database/seed.sql
```

### Step 3: Configure Environment Variables

```bash
cd backend
cp .env.example .env
```

Open `backend/.env` and fill in your MySQL credentials:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=YOUR_ACTUAL_PASSWORD
DB_NAME=research_portal
FLASK_PORT=5000
FLASK_DEBUG=True
```

> **⚠️ Never commit the `.env` file.** It is already in `.gitignore`.

### Step 4: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 5: Start the Backend Server

```bash
cd backend
python app.py
```

You should see:

```
🚀 Research Opportunity Portal API running on http://localhost:5000
```

### Step 6: Open the Frontend

Open `frontend/index.html` directly in your browser:

- **Windows:** Double-click the file, or run:
  ```bash
  start frontend/index.html
  ```
- **macOS:** `open frontend/index.html`
- **Linux:** `xdg-open frontend/index.html`

The portal should load and display any existing opportunities from the database.

---

## API Documentation

All endpoints use JSON request/response bodies.

| Method | Endpoint                    | Description              | Success | Error Codes  |
|--------|-----------------------------|--------------------------|---------|--------------|
| POST   | `/api/opportunities`        | Create a new opportunity | 201     | 400, 500     |
| GET    | `/api/opportunities`        | List all opportunities   | 200     | 500          |
| GET    | `/api/opportunities/:id`    | Get one by ID            | 200     | 404, 500     |
| PUT    | `/api/opportunities/:id`    | Update (partial or full) | 200     | 400, 404, 500|
| DELETE | `/api/opportunities/:id`    | Delete by ID             | 200     | 404, 500     |

### Request Body Fields (POST / PUT)

| Field                  | Type    | Required (POST) | Validation                        |
|------------------------|---------|------------------|-----------------------------------|
| `title`                | string  | ✅               | Max 200 characters                |
| `description`          | string  | ✅               | Non-empty                         |
| `research_area`        | string  | ✅               | Max 100 characters                |
| `faculty_name`         | string  | ✅               | Max 100 characters                |
| `department`           | string  | ✅               | Max 100 characters                |
| `required_skills`      | string  | ✅               | Max 500 characters                |
| `positions_available`  | integer | ✅               | Must be ≥ 0                       |
| `application_deadline` | string  | ✅               | Format: YYYY-MM-DD                |
| `status`               | string  | ❌ (PUT only)    | Must be "Open" or "Closed"        |

### Error Response Format

```json
{ "error": "Human-readable error message" }
```

---

## Postman Collection

1. Open Postman
2. Click **Import** → **Upload Files**
3. Select `postman/Research_Opportunity_Portal.postman_collection.json`
4. The collection includes 11 requests — run them sequentially to test:
   - Create 3 opportunities
   - Get all / Get one by ID
   - Update one
   - Close one (status → Closed)
   - Delete one
   - Request deleted one (404)
   - Send invalid data (400)

---

## Security Notes

- ✅ No real credentials are committed to the repository
- ✅ `.env` is listed in `.gitignore`
- ✅ All SQL queries use parameterized statements (no SQL injection)
- ✅ HTML output is escaped to prevent XSS
- ✅ Server errors return generic messages (no stack traces leaked)

---

## License

This project was created as a university assignment. All rights reserved.
