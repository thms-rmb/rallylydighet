from rallylydighet.db import get_db

def new_sequence(classes=None):
    query_template = """INSERT INTO sequence_sign (sequence_id, sign_id, priority)
                        SELECT {} AS sequence_id,
                               sign.id AS sign_id,
                               ROW_NUMBER() OVER(ORDER BY RANDOM()) AS priority
                        FROM sign
                        WHERE {}
                        ORDER BY priority"""

    if classes is None:
        classes = {"1", "2", "3", "4"}

    classes = classes & {"1", "2", "3", "4"}

    db = get_db()

    with db:
        cursor = db.cursor()

        cursor.execute("INSERT INTO sequence DEFAULT VALUES")
        rowid = cursor.lastrowid
        
        query = query_template.format(rowid,
                                      " OR ".join(["sign.code LIKE ?" for _ in classes]))
        params = tuple(c + "%" for c in classes)
        cursor.execute(query, params)

        db.commit()

    return rowid

def get_sequence_signs(sequence_id):
    query = """SELECT sequence_sign.sign_id AS id,
                      sign.code AS code,
                      sequence_sign.priority AS priority
               FROM sequence_sign
               INNER JOIN sign ON sign.id = sequence_sign.sign_id
                      AND sequence_sign.sequence_id = ?
               ORDER BY sequence_sign.priority"""
    
    db = get_db()
    
    signs = db.execute(query, (sequence_id,)).fetchall()
    
    return signs

def get_sequence(sequence_id):
    query = "SELECT id, created FROM sequence WHERE id = ?"

    db = get_db()

    sequence = db.execute(query, (sequence_id,)).fetchone()

    return sequence
