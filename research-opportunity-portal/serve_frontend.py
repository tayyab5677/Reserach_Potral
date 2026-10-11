"""
serve_frontend.py — Simple HTTP Server for the Frontend
=========================================================
Serves the frontend/ folder on http://localhost:8080
Run this alongside the Flask backend (port 5000).

Usage:
    python serve_frontend.py
"""

import http.server
import socketserver
import os

PORT = 8080
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')

os.chdir(FRONTEND_DIR)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"[OK] Frontend running at http://localhost:{PORT}")
    print(f"     Serving files from: {FRONTEND_DIR}")
    print(f"     Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[STOPPED] Frontend server stopped.")
