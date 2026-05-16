from flask import Flask, render_template, request, redirect, session
import sqlite3
import requests

app = Flask(__name__)
app.secret_key = "secretkey"
DB = "books.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            pages INTEGER,
            rating REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "password":
            session["user"] = "admin"
            return redirect("/")
        return "Invalid login"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    error = None

    if request.method == "POST":
        isbn = request.form["isbn"]
        try:
            url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
            data = requests.get(url).json()

            if "items" not in data:
                error = "No book found"
            else:
                book = data["items"][0]["volumeInfo"]
                title = book.get("title", "N/A")
                author = ", ".join(book.get("authors", ["N/A"]))
                pages = book.get("pageCount", 0)
                rating = book.get("averageRating", 0)

                c.execute("INSERT INTO books (title, author, pages, rating) VALUES (?, ?, ?, ?)",
                          (title, author, pages, rating))
                conn.commit()
        except:
            error = "Error processing data"

    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()

    return render_template("index.html", books=books, error=error)

@app.route("/delete/<int:book_id>")
def delete(book_id):
    if "user" not in session:
        return redirect("/login")
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
