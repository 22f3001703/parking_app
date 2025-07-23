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
            new_user = User(email=email,fullname=fullname,password=password,address=address,pincode=pincode,role="user")
            db.session.add(new_user)
            db.session.commit()
            print("sita")
            return redirect("/login")
    return render_template("register.html")    




@controllers.route("/login", methods=['GET','POST'])
def login():
    print("Starting the login")
    if request=='POST':
        email = request.form.get("email")
        password= request.form.get("password")
    

        if not email or not password:
            flash("Plaese provide both email and password","danger")
            return render_template("login.html")

    return render_template('login.html')