You are a senior full-stack developer helping me finish a university assignment: a "University Research Opportunity Portal". Build the complete project, working in the order below. Do not skip the planning stages.

## 1. PROBLEM
Research opportunities at my university are shared through emails, WhatsApp groups, and noticeboards, so students miss them and faculty struggle to manage them. I need a web app where faculty can post, view, update, and manage research opportunities in one place. It needs a backend REST API, a MySQL database, and a simple frontend.

## 2. REQUIREMENTS

### Data fields (each opportunity)
- id (unique, auto-increment)
- title
- description
- research_area
- faculty_name
- department
- required_skills
- positions_available (integer)
- application_deadline (date)
- status (Open or Closed)

### REST API (all operations must use the database, no hard-coded data)
- POST   /api/opportunities       -> create (201)
- GET    /api/opportunities       -> list all (200)
- GET    /api/opportunities/:id   -> get one (200 / 404)
- PUT    /api/opportunities/:id   -> update, including status change Open -> Closed (200 / 400 / 404)
- DELETE /api/opportunities/:id   -> delete (200 / 404)

Status codes to use: 200, 201, 400 (invalid or missing data), 404 (not found), 500 (server error).

### Frontend (simple, clean, functional)
1. Display all opportunities
2. View full details of a selected opportunity
3. Form to create a new opportunity
4. Option to update an existing opportunity
5. Button to change status from Open to Closed
6. Option to delete (with confirmation)
7. Show success and error messages
8. Basic validation of required form fields
All data must come from the API through fetch(). Nothing hard-coded.

### Technology
- Backend: Python (Flask) + flask-cors
- Database: MySQL (use mysql-connector-python or PyMySQL, parameterized queries only)
- Frontend: HTML, CSS, JavaScript, Bootstrap (no build step)
- Credentials in a .env file (never committed). Provide .env.example and .gitignore.

### Deliverables
- Backend and frontend source code
- Database schema/setup file (schema.sql, optionally seed.sql with sample rows)
- Exported Postman or Bruno collection (JSON)
- README.md with setup and run instructions and a placeholder for the GitHub repo link
- A one-minute demo video script (I will record the video myself)
- Final ZIP named: P24-0000_NAME_CLASS.zip (I will replace the placeholders)

## 3. PLAN
Give me a short step-by-step plan with milestones before writing code. Each milestone should map to one meaningful Git commit (e.g. "Add database schema", "Implement create endpoint", "Add frontend list view"). Provide the exact git commands for each commit so I do not upload everything in one commit.

## 4. ARCHITECTURE
Show the folder structure, for example:

research-opportunity-portal/
  backend/ (app.py, db.py, validators.py, requirements.txt, .env.example)
  frontend/ (index.html, css/, js/)
  database/ (schema.sql, seed.sql)
  postman/ (collection JSON)
  README.md
  .gitignore

Briefly explain how the frontend, API, and database communicate.

## 5. DATA MODEL
Provide the MySQL CREATE TABLE statement with appropriate types, NOT NULL constraints, an ENUM('Open','Closed') for status with default 'Open', and a CHECK or validation for positions_available >= 0.

## 6. SYSTEM DESIGN
- Document every endpoint: request body, example response, and status codes.
- Server-side validation rules: required fields, positions must be a non-negative integer, deadline must be a valid date (YYYY-MM-DD), status must be Open or Closed. Return 400 with a clear JSON error message listing the problems.
- Consistent JSON error format, e.g. {"error": "message"}.
- Global error handling that returns 500 for unexpected errors without leaking internals.
- Handle a PUT/DELETE/GET on a non-existent ID with 404.

## 7. IMPLEMENTATION
Write complete, working, commented code for every file: backend, schema, frontend (list, details view, create/edit form, close button, delete with confirm, Bootstrap alerts for success/error, client-side validation).

## 8. TESTING
Create the Postman (or Bruno) collection covering:
1. Create at least 3 opportunities
2. Get all
3. Get one by ID
4. Update one
5. Change status Open -> Closed
6. Delete one
7. Request the deleted one again (404)
8. Send one invalid/missing-data request (400)
Give me the importable collection JSON and the manual test steps.

## 9. README.md
Include: project overview, features, tech stack, folder structure, prerequisites, step-by-step setup (create MySQL database, run schema.sql, create .env, install requirements, run backend, open frontend), API documentation table, how to import the Postman/Bruno collection, GitHub repo link placeholder, and a note that no credentials are committed.

## 10. DEMO VIDEO SCRIPT
Write a script that fits in 60 seconds and covers, in order: backend running, frontend running, create, list, update, close, delete, one validation or 404 error, and API requests/responses in Postman/Bruno.

## RULES
- Original, clean code only. Keep it simple and beginner-readable.
- No hard-coded data in the frontend, and all CRUD must hit MySQL.
- Never include real passwords or API keys.
- After finishing, give me a final checklist matching the assignment's submission requirements and the commands to create the ZIP.