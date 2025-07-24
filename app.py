from flask import Flask 
from database import db 
from controllers.controllers import controllers




def create_app():
    app = Flask(__name__)
    app.debug=True
    app.config["SQLALCHEMY_DATABASE_URI"]= 'sqlite:///parking.db'
    db.init_app(app)
    app.app_context().push()
    app.register_blueprint(controllers)
    app.secret_key = "123456"
    return app

app = create_app()



if __name__ == "__main__":
    app.run()