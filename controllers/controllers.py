from flask import Flask,render_template,redirect,request,Response,Blueprint,session


from database import db
from models.models import User
from models.models import ParkingLot
from models.models import ParkingSpot
from models.models import ReserveParkingSpot
from datetime import datetime 



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
            return render_template("duplicate.html")
            
        if(theUser.password==password):
            print("Logged in succesfully🍀")
            
            if(theUser.role=="admin"):
                theUser.status=1
                db.session.commit()
                session['id']=theUser.id
                session["fullname"]=theUser.fullname
                session["role"]=theUser.role
                session["email"]=theUser.email
                session["status"]=theUser.status
                
                print("redirecting to dashboard")
                return redirect("/admin/dashboard")
            else:
                theUser.status=1
                db.session.commit()
                session['id']=theUser.id
                session["fullname"]=theUser.fullname
                session["role"]=theUser.role
                session["email"]=theUser.email
                session["status"]=theUser.status
                print("redirecting to dashboard")
                return redirect("/user/dashboard")
        
    return render_template('login.html')


@controllers.route("/admin/dashboard", methods=['GET','POST'])
def admindashboard():
    status = session.get("status")
    if status is not None and int(status) > 0:
        parkingspot=ParkingSpot.query.all()

        lotandspotstructure={}
        for spot in parkingspot:
            if spot.lotid not in lotandspotstructure:
                lotandspotstructure[spot.lotid]=[]
            lotandspotstructure[spot.lotid].append(spot)    

        distinctlotids=list(lotandspotstructure.keys())    
        lots=ParkingLot.query.filter(ParkingLot.id.in_(distinctlotids)).all()


        thefinalcards=[]
        for lot in lots:
            thefinalcards.append(

                {
                    'lot': lot,
                    'spots': lotandspotstructure[lot.id]
                }
            )


        print("ram")
        

        return render_template("admindashboard.html",fullname=session["fullname"]
                            ,status=session["status"],
                            role=session["role"],thefinalcards=thefinalcards)
    
    else:
        return redirect("/login")


@controllers.route("/admin/dashboard/users", methods=['GET','POST'])
def userDetails():
    status = session.get("status")
    if status is not None and int(status) > 0:
        getuser = User.query.filter_by(role="user")
        
        for i in getuser:
            print(i.pincode)
        print("executed")    
        return render_template("userDetails.html",getuser=getuser)
    else:
        return redirect("/login")

@controllers.route("/admin/dashboard/summary", methods=['GET','POST'])
def summary():
    status = session.get("status")
    if status is not None and int(status) > 0:
        return render_template("summary.html")
    else:
        return redirect("/login")


@controllers.route("/admin/dashboard/search", methods=['GET','POST'])
def search():
    query=None
    querytype=None
    pattey=[]
    status = session.get("status")
    if status is not None and int(status) > 0:
        if request.method=="POST":
            querytype = request.form.get("querytype")
            query = request.form.get("query")


            if querytype=="location":
                querydata=ParkingLot.query.filter(ParkingLot.location_name.ilike(f"%{query}")).all()
            elif querytype == "pincode":
                querydata= ParkingLot.query.filter(ParkingLot.pincode==int(query)).all()    
            else:
                querydata=[]

            querydataids= [query.id for query in querydata ] 

            thespot = ParkingSpot.query.filter(ParkingSpot.lotid.in_(querydataids)).all()  

            spotstructure={}

            for s in thespot:
                spotstructure.setdefault(s.lotid,[]).append(s)

            pattey=[]

            for x in querydata:
                pattey.append({
                    "lot":x,
                    "spots":spotstructure.get(x.id,[])
                })  
        return render_template("search.html",query=query,pattey=pattey)
    else:
        return redirect("/login")


@controllers.route("/admin/dashboard/addparkinglot", methods=['GET','POST'])
def addParkingLot():
    status = session.get("status")
    if status is not None and int(status) > 0:
        if request.method=='POST':
            location_name=request.form.get("location_name")
            address = request.form.get("address")
            pincode= request.form.get("pincode")
            price= request.form.get('price')
            max_spots=request.form.get("max_spots")

            newParkingLot= ParkingLot(location_name=location_name,address=address,pincode=pincode,price=price,max_spots=max_spots,occupied=0)
            db.session.add(newParkingLot)
            db.session.commit()


            for _ in range(int(max_spots)):
                newSpot=ParkingSpot(
                    lotid=newParkingLot.id,
                    status="A",
                    veichleNumber=None
                    )
                db.session.add(newSpot)
            db.session.commit()
            return redirect("/admin/dashboard")
            
        return render_template("addParkingLot.html")
    else:
        return redirect("/login")


@controllers.route("/admin/dashboard/editlot/<int:lot_id>", methods=['GET','POST'])
def editParkingLot(lot_id):
    status = session.get("status")
    if status is not None and int(status) > 0:
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
    else:
        return redirect("/login")

@controllers.route("/admin/dashboard/deletelot/<int:lot_id>", methods=['GET','POST'])
def deleteParkingLOt(lot_id):
    status = session.get("status")
    if status is not None and int(status) > 0:
        parkinglot = ParkingLot.query.get_or_404(lot_id)
        if(parkinglot.occupied>0):
            print("Encountered")
            return render_template("deleteerror.html")
        db.session.delete(parkinglot)
        db.session.commit()
        return redirect("/admin/dashboard")
    else:
        return redirect("/login")


@controllers.route("/user/dashboard", methods=['GET','POST'])
def userdashboard():
    status = session.get("status")
    if status is not None and int(status) > 0:

        useremail=session.get("email")

        recentParkingHistory = db.session.query(
            ReserveParkingSpot.id,
            ReserveParkingSpot.lotid,
            ReserveParkingSpot.spotid,
            ReserveParkingSpot.parking_time,
            ReserveParkingSpot.ispaid,
            ReserveParkingSpot.veichleNumber,
            ParkingLot.location_name
        ).join(ParkingLot,ReserveParkingSpot.lotid==ParkingLot.id)\
        .filter(ReserveParkingSpot.email==useremail)\
        .all()




        return render_template("userdashboard.html",recentParkingHistory=recentParkingHistory)
    else:
        return redirect("/login")


@controllers.route("/user/dashboard/searchandbook", methods=['GET','POST'])
def searchAndBook():
    status = session.get("status")
    if status is not None and int(status) > 0:
        if request.method=="POST":
            querytype=request.form.get("querytype")
            query=request.form.get("query")
            if querytype=="pincode":
                search_result = ParkingLot.query.filter_by(pincode=query).all()
                for i in search_result:
                    print(i)
                return render_template("userSearchandBook.html",search_result=search_result,querytype=querytype)    
            else:
                search_result=ParkingLot.query.filter_by(location_name=query).all() 
                for i in search_result:
                    print(i) 
                return render_template("userSearchandBook.html",search_result=search_result,querytype=querytype)      
        return render_template("userSearchandBook.html")    
    else:
        return redirect("/login")

@controllers.route("/user/dashboard/summary", methods=['GET','POST'])
def userSummary():
    status = session.get("status")
    if status is not None and int(status) > 0:
    
        return render_template("userSummary.html")
    else:
        return redirect("/login")


@controllers.route("/user/dashboard/booknow/<int:id>", methods=['GET','POST'])
def bookNow(id):
    status = session.get("status")
    if status is not None and int(status) > 0:
        freespots=ParkingSpot.query.filter_by(lotid=id,status='A').with_entities(ParkingSpot.id).all()
        avaspots=[spot_id for (spot_id,) in freespots]


        for spot_id in avaspots:
            print(spot_id)

        if(request.method=="POST"):
            print("post")  
            spotid=request.form.get("spot_id")
            lotid=request.form.get("lotid")
            email=request.form.get("email")
            parking_time=datetime.utcnow()
            veichleNumber=request.form.get("veichle")


            spot = ParkingSpot.query.filter_by(id=spotid, lotid=lotid).first()
            if spot:
                spot.veichleNumber=veichleNumber 
                db.session.commit()


            reserveparkingspot= ReserveParkingSpot(
                
                spotid=spotid,
                lotid=lotid,
                email=email,
                parking_time=parking_time,
                veichleNumber=veichleNumber
                
            )
            db.session.add(reserveparkingspot)
            db.session.commit()

            return redirect("/user/dashboard")

        return render_template("bookParking.html",avaspots=avaspots , id = id )
    else:
        return redirect("/login")



@controllers.route("/user/dashboard/reservethespot", methods=['GET','POST'])

def reserveaspot():
    status = session.get("status")
    if status is not None and int(status) > 0:
        if(request.method=="POST"):
            print("post")  
            spotid=request.form.get("spot_id")
            lotid=request.form.get("lotid")
            email=request.form.get("email")
            parking_time=datetime.utcnow()
            veichleNumber=request.form.get("veichle")

            abc= ParkingLot.query.filter_by(id=lotid).first()

            currentoccupancy=int(abc.occupied)


            spot = ParkingSpot.query.filter_by(id=spotid, lotid=lotid).first()
            if spot:
                spot.veichleNumber=veichleNumber
                spot.status="O"
                db.session.commit()

            abc.occupied=currentoccupancy+1    
            db.session.commit()


            reserveparkingspot= ReserveParkingSpot(
                
                spotid=spotid,
                lotid=lotid,
                email=email,
                parking_time=parking_time,
                ispaid=0,
                veichleNumber=veichleNumber
            
                
            )
            db.session.add(reserveparkingspot)
            db.session.commit()

            return redirect("/user/dashboard")
    else:
        return redirect("/login")    
    

@controllers.route("/user/dashboard/releasespot/<int:id>", methods=['GET','POST'])
def releasespot(id):
    status = session.get("status")
    if status is not None and int(status) > 0:
        thereservation = ReserveParkingSpot.query.get_or_404(id)
        release_time=datetime.utcnow()
        duration = release_time-thereservation.parking_time
        timeinhours=int(duration.total_seconds()//3600)

        if duration.total_seconds()%3600!=0:
            timeinhours+=1
        thelot = ParkingLot.query.get(thereservation.lotid)
        totalfare=timeinhours*thelot.price
        if request.method=="POST":
            thereservation = ReserveParkingSpot.query.get_or_404(id)
            

            thespot = ParkingSpot.query.get(thereservation.spotid)
            

            if thespot and thelot and thereservation.ispaid==0:
                thespot.status="A"
                thespot.veichleNumber=None
                

                thereservation.release_time=release_time
                thereservation.ispaid=1
                thereservation.parkingcost=totalfare

                thelot.occupied-=1
                db.session.commit()
                return redirect("/user/dashboard")

        return render_template("releaseSpot.html",thereservation=thereservation,release_time=release_time,totalfare=totalfare,id=id)
    else:
        return redirect("/login")

@controllers.route("/admin/dashboard/view/<int:id>",methods=["GET","POST"])
def viewSpot(id):
    status = session.get("status")
    if status is not None and int(status) > 0:
        spotDetails = ParkingSpot.query.filter_by(id=id).first()
        print("here")
        return render_template("viewSpot.html",spotDetails=spotDetails)
    else:
        return redirect("/login")


@controllers.route("/admin/dashboard/view/extradetail/<int:id>",methods=["GET","POST"])
def viewSpotInExtraDetail(id):
    status = session.get("status")
    if status is not None and int(status) > 0:
        spotDetails = ParkingSpot.query.filter_by(id=id).first()
        
        reservationdetails=ReserveParkingSpot.query.filter_by(lotid=spotDetails.lotid,spotid=spotDetails.id).first()
        if not reservationdetails:
            reservationdetails={
                "email":"None",
                "parking_time":"None"
            }
        
        parkingdetails= ParkingLot.query.filter_by(id=spotDetails.lotid).first()
    

        return render_template("viewSpotInExtraDetails.html",spotDetails=spotDetails,reservationdetails=reservationdetails,parkingdetails=parkingdetails)
    else:
        return redirect("/login")


##### i have to create a flow for delteing the spot completely
@controllers.route("/admin/dashboard/view/delete/<int:id>",methods=["post","get"])
def deletethespot(id):
    status = session.get("status")
    if status is not None and int(status) > 0:
        spotDetails = ParkingSpot.query.filter_by(id=id).first()
        parkingdetails= ParkingLot.query.filter_by(id=spotDetails.lotid).first()

        if(spotDetails.status=="A"):
            parkingdetails.max_spots-=1
            db.session.delete(spotDetails)
            db.session.commit()
        else:
            return render_template("deletespot.html")    

        return redirect ("/admin/dashboard")
    else:
        return redirect("/login")




@controllers.route("/logout/<int:id>",methods=["GET","POST"])
def logout(id):
    status = session.get("status")
    if status is not None and int(status) > 0:
        if request.method=="POST":
            theuser= User.query.get("id")
            if theuser:
                theuser.status = 0
                db.session.commmit()

        session.clear()
    return redirect("/login")        

@controllers.route("/editprofile/<int:id>",methods=["GET","POST"])
def editProfile(id):
    status = session.get("status")
    if status is not None and int(status) > 0:
        theuser=User.query.get(id)
        print(theuser.fullname)
        if not theuser:
            return "User not found", 404
        
        if request.method=="POST":
            theuser.fullname=request.form.get("fullname")
            theuser.address=request.form.get("address")
            theuser.pincode=request.form.get("pincode")
            theuser.email=request.form.get("email")
            theuser.password=request.form.get("password")
            db.session.commit()
            print("done")
            return redirect(f"/{session.get('role')}/dashboard")

        return render_template("editProfile.html",theuser=theuser)
    else:
        return redirect("/login")
    


