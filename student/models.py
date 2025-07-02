from einvoicing import db

class Student(db.Model):
    __tablename__ = 'hep_students'  # Explicit, avoids reserved keyword
    
    id = db.Column(db.Integer, primary_key=True)
    matric_no = db.Column(db.String(15))
    name = db.Column(db.String(255))
    email_1 = db.Column(db.String(50))
    email_2 = db.Column(db.String(50))
    prog_code = db.Column(db.String(10))
    prog_name = db.Column(db.String(200))
    ic_no = db.Column(db.String(12))
    phone_no = db.Column(db.String(20))
    gender = db.Column(db.String(1))
    semester = db.Column(db.String(10))
    session = db.Column(db.String(10))