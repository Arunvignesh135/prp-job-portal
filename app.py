from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB_NAME = "jobs.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT NOT NULL,
            email TEXT NOT NULL,
            job_id INTEGER NOT NULL
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM jobs"
    ).fetchone()[0]

    if count == 0:
        conn.execute(
            "INSERT INTO jobs (title, company, location) VALUES (?, ?, ?)",
            ("DevOps Engineer", "ABC Technologies", "Chennai")
        )

        conn.execute(
            "INSERT INTO jobs (title, company, location) VALUES (?, ?, ?)",
            ("Cloud Engineer", "XYZ Solutions", "Bangalore")
        )

        conn.execute(
            "INSERT INTO jobs (title, company, location) VALUES (?, ?, ?)",
            ("Python Developer", "TechSoft", "Hyderabad")
        )

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/jobs")
def jobs():
    conn = get_db_connection()
    jobs = conn.execute("SELECT * FROM jobs").fetchall()
    conn.close()

    return render_template("jobs.html", jobs=jobs)


@app.route("/apply/<int:job_id>", methods=["GET", "POST"])
def apply(job_id):

    if request.method == "POST":
        candidate_name = request.form["candidate_name"]
        email = request.form["email"]

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO applications
            (candidate_name, email, job_id)
            VALUES (?, ?, ?)
            """,
            (candidate_name, email, job_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("jobs"))

    return render_template("apply.html", job_id=job_id)


@app.route("/health")
def health():
    return {"status": "UP"}, 200


if __name__ == "__main__":
    create_database()

    app.run(
        host="0.0.0.0",
        port=5000
    )
