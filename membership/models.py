from einvoicing import db

class Membership(db.Model):
    __tablename__ = 'memberships'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('hep_students.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('clb_clubs.id'), nullable=False) 
    reg_date = db.Column(db.DateTime(timezone=True), nullable=False)
    reg_duration = db.Column(db.Integer, nullable=False)

    student = db.relationship('Student', backref='memberships')
    club = db.relationship('Club', backref='memberships')
