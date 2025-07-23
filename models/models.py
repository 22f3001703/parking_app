from database import db

class User(db.Model):
    id= db.Column(db.Integer(),primary_key=True)
    fullname = db.Column(db.String(50),nullable = False)
    email = db.Column(db.String(50),unique = True,nullable = False)
    password = db.Column(db.String(),nullable= False)
    address = db.Column(db.String(200),nullable=False)
    pincode = db.Column(db.Integer(),nullable= False)
    role = db.Column(db.String(10),nullable=False)
    status=db.Column(db.Integer(),nullable=False)



