from rallylydighet.db import get_db

def get_sign(sign_id):
    query = "SELECT * FROM sign WHERE id = ?"

    db = get_db()

    sign = db.execute(query, (sign_id,)).fetchone()

    return sign

def insert_sign(code, mime, size, content):
    query = """INSERT INTO sign (code, mime, size, content)
               VALUES (?, ?, ?, ?)"""

    db = get_db()
    
    db.execute(query, (code, mime, size, content))
    db.commit()
