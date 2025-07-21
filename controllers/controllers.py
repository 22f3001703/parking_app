from flask import Flask,render_template,redirect,request,Response,Blueprint


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
        print("ram")
        emailexsist=User.query.filter_by(email=email).first()
        print("shtam")
        if(emailexsist):
            return render_template("duplicate.html")
        else:
            new_user = User(email=email,fullname=fullname,password=password,address=address,pincode=pincode)
            db.session.add(new_user)
            db.session.commit()
            print("sita")
            return redirect("/login")
    return render_template("register.html")    
