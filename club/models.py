from einvoicing import db

class Club(db.Model):
    __tablename__ = 'clb_clubs'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    name = db.Column(db.String(100), nullable=False)
    advisor = db.Column(db.String(100), nullable=False)