from flask import Flask,render_template,redirect,request,Response,Blueprint,session


from database import db
from models.models import User
from models.models import ParkingLot



controllers = Blueprint('controllers', __name__)
@controllers.route("/register", methods=['GET','POST'])
def register():
    print(">>> Register route hit")
    if request.method=="POST":
        fullname= request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
 
        emailexsist=User.query.filter_by(email=email).first()
       
        if(emailexsist):
            return render_template("duplicate.html")
        else:
            new_user = User(email=email,fullname=fullname,password=password,address=address,pincode=pincode,role="user",status=0)
            db.session.add(new_user)
            db.session.commit()
            print("sita")
            return redirect("/login")
    return render_template("register.html")    




@controllers.route("/login", methods=['GET','POST'])
def login():
    print("Starting the login")
    if request.method=='POST':
        email = request.form.get("email")
        password= request.form.get("password")
    
        print(email)
        print(password)

        if not email or not password:
            return render_template("duplicate.html")
        
        theUser = User.query.filter_by(email=email).first()
        if not theUser:
            render_template("duplicate.html")
            return render_template("register.html") 
        if(theUser.password==password):
            print("Logged in succesfully🍀")
            
            if(theUser.role=="admin"):
                theUser.status=1
                db.session.commit()
                session['id']=theUser.id
                session["fullname"]=theUser.fullname
                session["role"]=theUser.role
                session["status"]=theUser.status
                
                print("redirecting to dashboard")
                return redirect("/admin/dashboard")
            else:
                theUser.status=1
                db.session.commit()
                session['id']=theUser.id
                session["fullname"]=theUser.fullname
                session["role"]=theUser.role
                session["status"]=theUser.status
                print("redirecting to dashboard")
                return redirect("/user/dashboard")
        
    return render_template('login.html')


@controllers.route("/user/dashboard", methods=['GET','POST'])
def userdashboard():
    return render_template("dashboard.html")



@controllers.route("/admin/dashboard", methods=['GET','POST'])
def admindashboard():
    parkinglot=ParkingLot.query.all()
    print("ram")
    

    return render_template("admindashboard.html",fullname=session["fullname"]
                           ,status=session["status"],
                           role=session["role"],parkinglot=parkinglot)


@controllers.route("/admin/dashboard/users", methods=['GET','POST'])
def userDetails():
    getuser = User.query.filter_by(role="user")
    
    for i in getuser:
        print(i.pincode)
    print("executed")    
    return render_template("userDetails.html",getuser=getuser)

@controllers.route("/admin/dashboard/summary", methods=['GET','POST'])
def summary():
    return render_template("summary.html")

@controllers.route("/admin/dashboard/search", methods=['GET','POST'])
def search():
    return render_template("search.html")


@controllers.route("/admin/dashboard/addparkinglot", methods=['GET','POST'])
def addParkingLot():
    if request.method=='POST':
        location_name=request.form.get("location_name")
        address = request.form.get("address")
        pincode= request.form.get("pincode")
        price= request.form.get('price')
        max_spots=request.form.get("max_spots")

        newParkingLot= ParkingLot(location_name=location_name,address=address,pincode=pincode,price=price,max_spots=max_spots,occupied=0)
        db.session.add(newParkingLot)
        db.session.commit()

        return redirect("/admin/dashboard")
        
    return render_template("addParkingLot.html")


@controllers.route("/admin/dashboard/editlot/<int:lot_id>", methods=['GET','POST'])
def editParkingLot(lot_id):
    parkinglot=ParkingLot.query.get_or_404(lot_id)
    if request.method=="POST":
        parkinglot.location_name = request.form.get("location_name")
        parkinglot.address=   request.form.get("address")
        parkinglot.pincode= request.form.get("pincode")
        parkinglot.price= request.form.get("price")
        parkinglot.max_spots = request.form.get("max_spots")
        db.session.commit()
        return redirect("/admin/dashboard")
    return render_template("editParkingLot.html",parkinglot=parkinglot)


@controllers.route("/admin/dashboard/deletelot/<int:lot_id>", methods=['GET','POST'])
def deleteParkingLOt(lot_id):
    parkinglot = ParkingLot.query.get_or_404(lot_id)
    db.session.delete(parkinglot)
    db.session.commit()
    return redirect("/admin/dashboard")