from db import db

def add_test(topic, created_at):
    if not topic or created_at == None:
        return 0
    try:
        sql = "INSERT INTO Tests (topic, created_at) VALUES (:topic, now()) RETURNING id"
        result = db.session.execute(sql, {"topic":topic})
        db.session.commit()
        exercise_id = result.fetchone()[0]
        return exercise_id
    except:
        return 0