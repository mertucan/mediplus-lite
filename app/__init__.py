from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babel import Babel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
admin = Admin()
babel = Babel()
login_manager = LoginManager(app)
login_manager.init_app(app)
admin.init_app(app)
babel.init_app(app)

from app import views, models, db
from app.models import User, Appointment, Doctors, Messages, Blogs

if not 'User' in locals():
    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), index=True, unique=True)
        email = db.Column(db.String(120), index=True, unique=True)
        password_hash = db.Column(db.String(128))

        def __repr__(self):
            return '<User {}>'.format(self.username)

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password_hash, password)
    
admin.add_view(ModelView(User, db.session))

if not 'Doctors' in locals():
    class Doctors(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), index=True, unique=True)
        department = db.Column(db.String(64), index=True)
        
admin.add_view(ModelView(Doctors, db.session))

if not 'Department' in locals():
    class Department(db.Model):
        __table_args__ = {'extend_existing': True}
        id = db.Column(db.Integer, primary_key=True)
        department = db.Column(db.String(64), index=True)
        
admin.add_view(ModelView(Department, db.session))

if not 'Appointment' in locals():
    class Appointment(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), index=True)
        email = db.Column(db.String(120), index=True)
        phone = db.Column(db.String(15), index=True)
        doctor_name = db.Column(db.String(64), index=True)
        date = db.Column(db.Date, index=True)
        message = db.Column(db.String(256), index=True)
        
admin.add_view(ModelView(Appointment, db.session))

if not 'Messages' in locals():
    class Messages(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), index=True)
        email = db.Column(db.String(120), index=True)
        phone = db.Column(db.String(15), index=True)
        subject = db.Column(db.String(64), index=True)
        message = db.Column(db.String(512), index = True)
        
admin.add_view(ModelView(Messages, db.session))
        
if not 'BlogPost' in locals():
    class BlogPost(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), index=True)
        surname = db.Column(db.String(64), index=True)
        email = db.Column(db.String(120), index=True)
        message = db.Column(db.String(512), index = True)
        
admin.add_view(ModelView(Blogs, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

