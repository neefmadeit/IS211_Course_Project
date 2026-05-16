# IS211_Course_Project

Book Catalogue Web Application

This project is a Flask-based web application that allows users to keep track of books they own.

Features:
- User login (single user)
- Search for books using ISBN via Google Books API
- Store book details in SQLite database
- Display saved books
- Delete books

Database Model:
books(id, title, author, pages, rating)

How to run:
1. Install dependencies: pip install -r requirements.txt
2. Run: python app.py
3. Open browser at http://127.0.0.1:5000/login
