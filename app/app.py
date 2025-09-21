import os
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = os.environ.get("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# DB from env
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST","db"),
    user=os.environ.get("DB_USER","appuser"),
    password=os.environ.get("DB_PASS","apppass"),
    database=os.environ.get("DB_NAME","appdb")
)
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    filename VARCHAR(255)
)
""")
db.commit()

@app.route("/")
def index():
    return "Flask migration demo app is running!"

@app.route("/add_user", methods=["POST"])
def add_user():
    name = request.form.get("name")
    file = request.files.get("file")

    if not name or not file:
        return jsonify({"error": "Name and file required"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    cursor.execute("INSERT INTO users (name, filename) VALUES (%s, %s)", (name, file.filename))
    db.commit()

    return jsonify({"message": f"User {name} added with file {file.filename}"}), 201

@app.route("/users", methods=["GET"])
def list_users():
    cursor.execute("SELECT id, name, filename FROM users")
    rows = cursor.fetchall()
    users = [{"id": r[0], "name": r[1], "filename": r[2]} for r in rows]
    return jsonify(users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
