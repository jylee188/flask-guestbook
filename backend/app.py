
import os
import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def ensure_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guestbook (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.get("/api/guestbook")
def list_entries():
    try:
        with get_db() as conn:
            ensure_table(conn)
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id, name, message,
                        DATE_FORMAT(
                            created_at,
                            '%Y-%m-%d %H:%i:%s'
                        ) AS created_at
                    FROM guestbook
                    ORDER BY id DESC
                """)
                entries = cursor.fetchall()

        return jsonify(entries), 200

    except pymysql.MySQLError:
        app.logger.exception("Database read failed")
        return jsonify({"error": "Database unavailable"}), 503


@app.post("/api/guestbook")
def create_entry():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON 데이터가 필요합니다."}), 400

    name = str(data.get("name") or "").strip()
    message = str(data.get("message") or "").strip()

    if not name or not message:
        return jsonify({"error": "이름과 내용을 입력하세요."}), 400

    if len(name) > 50 or len(message) > 1000:
        return jsonify({"error": "입력 길이 초과"}), 400

    try:
        with get_db() as conn:
            ensure_table(conn)
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO guestbook (name, message) VALUES (%s, %s)",
                    (name, message)
                )
                new_id = cursor.lastrowid

        return jsonify({
            "id": new_id,
            "name": name,
            "message": message
        }), 201

    except pymysql.MySQLError:
        app.logger.exception("Database write failed")
        return jsonify({"error": "Database unavailable"}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

