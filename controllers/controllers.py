from flask import Flask,render_template,redirect,request,Response,Blueprint,flash


from database import db
from models.models import User



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
                print("redirecting to dashboard")
                return redirect("/admin/dashboard")
            else:
                theUser.status=1
                db.session.commit()
                print("redirecting to dashboard")
                return redirect("/user/dashboard")
        
    return render_template('login.html')


@controllers.route("/user/dashboard", methods=['GET','POST'])
def userdashboard():
    return render_template("dashboard.html")



@controllers.route("/admin/dashboard", methods=['GET','POST'])
def admindashboard():
    return render_template("admindashboard.html")