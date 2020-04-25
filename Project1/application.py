
import os
from flask import Flask, session, redirect, render_template, request, jsonify, flash ,url_for
from flask_session import Session
from sqlalchemy import create_engine
# from flask impor
from wtforms import StringField, PasswordField, BooleanField
from flask_wtf import FlaskForm
from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from models  import User

app = Flask(__name__,template_folder="templates")

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))





@app.route("/")
def index():
    return render_template("home.html") 

#--------------------------------------------------------------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get("username")
        password = request.form.get("password")
        details = User(username = name, password = password)
        db.add(details)
        db.commit()
        return render_template("success.html", message = "Successfully Registered")
    return render_template("register.html")    
       

#-------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        name = request.form.get("username")
        password = request.form.get("password")

        user = db.query(User).filter_by(username=name).first()
        if user:
            if user.password == password:
                return render_template("search.html")

        return render_template("error.html",message="Invalid username or password")        

    return render_template("login.html")






