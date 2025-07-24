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


class ParkingLot(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    location_name = db.Column(db.String(250),nullable=False)
    pincode=db.Column(db.Integer(),nullable=False)
    price=db.Column(db.Integer(),nullable=False)   
    max_spots=db.Column(db.Integer(),nullable=False) 
    address=db.Column(db.String(250),nullable=False)
    occupied=db.Column(db.Integer(),default=0)



