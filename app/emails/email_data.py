from ..database import *

def get_email_data(class_id: int):
    cursor.execute("""SELECT users.id, email, firstname, lastname FROM users, classes
    WHERE classes.student_id = users.id
    AND classes.id = %s
    """, (class_id,))
    student = cursor.fetchone()

    cursor.execute("""SELECT subject FROM classes WHERE id = %s""", (class_id,))
    subject = cursor.fetchone()

    cursor.execute("""
    SELECT  users.id, email, firstname, lastname
    FROM users, classes
    WHERE classes.tutor_id = users.id
    AND classes.id = %s
    """, (class_id,))

    tutor = cursor.fetchone()

    return student, tutor, subject