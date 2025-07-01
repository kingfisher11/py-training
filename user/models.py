from einvoicing import db

class User(db.Model):
    __tablename__ = 'users'  # Explicit, avoids reserved keyword
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))