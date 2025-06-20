from flask import Flask, render_template, request
import mysql.connector
import os
from datetime import date

app = Flask(__name__)

# Database Connection

db = mysql.connector.connect(
    host=os.environ['localhost'],
    user=os.environ['root'],
    password=os.environ[''],
    database=os.environ['dmart'],
    port=3306
)
cursor = db.cursor()

# Visitor Entry Page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        gender = request.form["gender"]
        age = request.form["age"]
        comment = request.form["comment"]
        cursor.execute("INSERT INTO visitors (gender, age, comment) VALUES (%s, %s, %s)",(gender, age, comment))
        db.commit()
        return render_template("index.html", message="✅ Submitted successfully!")
    return render_template("index.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    today = date.today()

    cursor.execute("SELECT COUNT(*) FROM visitors")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM visitors WHERE gender = 'male'")
    male = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM visitors WHERE gender = 'female'")
    female = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM visitors WHERE date = %s", (today,))
    today_visitors = cursor.fetchone()[0]

    return render_template("dashboard.html", total=total, male=male, female=female, today=today_visitors)

# View Filtered Visitors
@app.route("/view/<filter_type>")
def view_filtered(filter_type):
    if filter_type == "male":
        cursor.execute("SELECT * FROM visitors WHERE gender='male'")
        title = "Male Visitors"
    elif filter_type == "female":
        cursor.execute("SELECT * FROM visitors WHERE gender='female'")
        title = "Female Visitors"
    elif filter_type == "today":
        cursor.execute("SELECT * FROM visitors WHERE date=%s", (date.today(),))
        title = "Today's Visitors"
    else:
        cursor.execute("SELECT * FROM visitors")
        title = "All Visitors"

    records = cursor.fetchall()
    return render_template("view.html", records=records, title=title)

if __name__ == "__main__":
    app.run(debug=True)
