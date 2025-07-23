
from app import create_app
from database import db
from models.models import User

app = create_app()


with app.app_context():
    db.create_all()
    print("✅ Database and tables created!")
    print("creating admin")
    admin = User(
        fullname ="Aashish Jha",
        email = "jhaashish.ajha@gmail.com",
        password="error",
        address="Dhaula kuan",
        pincode = 110010,
        role="admin"
    )
    db.session.add(admin)
    db.session.commit()
    print("The admin is created succesfully🍀")


