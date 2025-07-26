from database import db
import datetime 

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


class ParkingSpot(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    lotid=db.Column(db.Integer(),nullable=False)
    status = db.Column(db.String(5),default="A")
    veichleNumber=db.Column(db.String(50),nullable=True)



class ReserveParkingSpot(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    spotid=db.Column(db.Integer(),nullable=False)
    lotid=db.Column(db.Integer(),nullable=False)
    userid=db.Column(db.Integer(),nullable=False)
    parking_time=db.Column(db.DateTime,nullable=False,default=datetime.UTC)
    release_time=db.Column(db.DateTime,nullable=False,default=datetime.UTC)
    parkingcost=db.Column(db.Integer(),nullable=False)


