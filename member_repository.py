import db


def list_members():
    conn = db.connect()
    try:
        return conn.execute("SELECT * FROM members").fetchall()
    finally:
        conn.close()


def get_member(member_id):
    conn = db.connect()
    try:
        return conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()
    finally:
        conn.close()


def get_member_by_email(email):
    conn = db.connect()
    try:
        return conn.execute("SELECT * FROM members WHERE email = ?", (email,)).fetchone()
    finally:
        conn.close()


def create_member(name, email, member_type):
    conn = db.connect()
    try:
        cur = conn.execute(
            "INSERT INTO members (name, email, type) VALUES (?, ?, ?)",
            (name, email, member_type),
        )
        conn.commit()
        return conn.execute("SELECT * FROM members WHERE id = ?", (cur.lastrowid,)).fetchone()
    finally:
        conn.close()
