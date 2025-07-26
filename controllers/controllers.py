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
    if(parkinglot.occupied>0):
        print("Encountered")
        return render_template("deleteerror.html")
    db.session.delete(parkinglot)
    db.session.commit()
    return redirect("/admin/dashboard")


@controllers.route("/user/dashboard", methods=['GET','POST'])
def userdashboard():

    useremail=session.get("email")

    recentParkingHistory = db.session.query(
        ReserveParkingSpot.id,
        ReserveParkingSpot.lotid,
        ReserveParkingSpot.spotid,
        ReserveParkingSpot.parking_time,
        ReserveParkingSpot.ispai,
        ReserveParkingSpot.veichleNumber,
        ParkingLot.location_name
    ).join(ParkingLot,ReserveParkingSpot.lotid==ParkingLot.id)\
    .filter(ReserveParkingSpot.email==useremail)\
    .all()




    return render_template("userdashboard.html",recentParkingHistory=recentParkingHistory)


@controllers.route("/user/dashboard/searchandbook", methods=['GET','POST'])
def searchAndBook():
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


@controllers.route("/user/dashboard/summary", methods=['GET','POST'])
def userSummary():
    
    return render_template("userSummary.html")


@controllers.route("/user/dashboard/booknow/<int:id>", methods=['GET','POST'])
def bookNow(id):
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


@controllers.route("/user/dashboard/reservethespot", methods=['GET','POST'])
def reserveaspot():
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
            ispai=0,
            veichleNumber=veichleNumber
           
            
        )
        db.session.add(reserveparkingspot)
        db.session.commit()

        return redirect("/user/dashboard")
    

@controllers.route("/user/dashboard/releasespot/<int:id>", methods=['GET','POST'])
def releasespot(id):
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
        

        if thespot and thelot and thereservation.ispai==0:
            thespot.status="A"
            thespot.veichleNumber=None
            

            thereservation.release_time=release_time
            thereservation.ispai=1
            thereservation.parkingcost=totalfare

            thelot.occupied-=1
            db.session.commit()
            return redirect("/user/dashboard")

    return render_template("releaseSpot.html",thereservation=thereservation,release_time=release_time,totalfare=totalfare,id=id)
   

@controllers.route("/admin/dashboard/view/<int:id>",methods=["GET","POST"])
def viewSpot(id):
    spotDetails = ParkingSpot.query.filter_by(id=id).first()
    print("here")
    return render_template("viewSpot.html",spotDetails=spotDetails)


@controllers.route("/admin/dashboard/view/extradetail/<int:id>",methods=["GET","POST"])
def viewSpotInExtraDetail(id):
    return render_template("viewSpotInExtraDetails.html")



