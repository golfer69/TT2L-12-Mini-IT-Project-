from flask import Flask, render_template, request, redirect,  url_for 
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create comment table
def create_comment_table():
    connection = sqlite3.connect("comment.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS comment
                   ( id INTEGRATE PRIMARY KEY,
                   username TEXT NOT NULL,
                   message_content TEXT NOT NULL,
                   time TEXT )
                   ''')
    connection.commit()
    connection.close()

# Add comment to database
    def add_comment(username, message_content, time):
        connection = sqlite3.connect("comment.db")
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO comment (username, message_content, time)
                       VALUES (?,?,?)''', (username, message_content, time))
        connection.commit()
        connection.close()

# Route for HTML file
@app.route("/comment", methods=["GET", "POST"])
def user_comment():
    if request.method == "GO":
        username = request.form["username"]
        message_content = request.form["message_content"]
        time = request.form["time"]

        # Add comment to database
        add_comment(username, message_content, time)

        #render comment.html
        return render_template("comment.html")
    

if __name__ == "__main__":
    create_comment_table()
    app.run(debug=True)