import os
from flask import Flask, session, redirect, render_template, request, jsonify, flash ,url_for
from flask_session import Session
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
# from flask impor
from wtforms import StringField, PasswordField, BooleanField
from flask_wtf import FlaskForm
from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models  import *
from books import *
from review import *

app = Flask(__name__,template_folder="templates")

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL")) 
db = scoped_session(sessionmaker(bind=engine))

#--------------------------------------------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("home.html") 

#--------------------------------------------------------------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get("username")
        password = request.form.get("password")
        hash_password=generate_password_hash(password,method='sha256')
        details = User(username = name, password = hash_password)
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
        hash_password=generate_password_hash(password,method='sha256')

        user = db.query(User).filter_by(username=name).first()
        if user:
            if check_password_hash(user.password,password):
                session['username']=name

                return render_template("search.html")

        return render_template("error.html",message="Invalid username or password")        

    return render_template("login.html")
#-------------------------------------------------------------------------------------------------------------------
@app.route('/search', methods=['GET','POST'])
def search():

    # Check book id was provided`
    if not request.args.get("book"):
        return render_template("error.html", message="you must provide a book.")

    # Take input and add a wildcard
    query = "%" + request.args.get("book") + "%"

    query = query.title()
    # rows= Book.query.filter(Books.isbn.LIKE(query) or Books.author.LIKE(query) or Books.title.LIKE(query) or Books.year.LIKE(query) ).all()
    rows = db.execute("SELECT isbn, title, author, year FROM book WHERE \
                        isbn LIKE :query OR \
                        title LIKE :query OR \
                        author LIKE :query LIMIT 15",
                        {"query": query})
    
    # Books not founded
    if rows.rowcount == 0:
        return render_template("error.html", message="we can't find books with that description.")
    
    # Fetch all the results
    books = rows.fetchall()

    return render_template("bookresult.html", books=books)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/review/<isbn>", methods =['GET', 'POST'])
def review(isbn):
    if session.get("username") is None:
        return redirect("/register")

    # isbn = "0380795272"
    book  = db.query(Book).filter_by(isbn = isbn).first()
    rating = db.query(Review).filter_by(title=book.title).all()
    # print("hello book name",book.isbn)
    
    # obj = db.query(User).get("Username")
    Uname = session.get("username")
    print(Uname) 
    if request.method == "POST":
        title = book.title
        rating1 = request.form.get("rate")
        review = request.form.get("comment")
        temp = Review(title,Uname,rating1,review)
        try:
            db.add(temp)
            db.commit() 
            ratin = db.query(Review).filter_by(title=book.title).all()
            return render_template("review.html",data = book, name = Uname, rating = ratin)
        except:
            db.rollback()
            return render_template("review.html", data = book, name = "Already given", rating = rating)
    else:
        return render_template("review.html",data = book, name = Uname ,rating = rating)

#-------------------------------------------------------------------------------------------------------------------------------------
# @app.route('/radio',methods=['GET','POST'])

# def route():

#         if request.method == 'POST' :     

#             request=''     
            
#             if request.form.get("isbn") == "option1":
#                 request='isbn'
#                 # By title 
#             elif request.form.get("book name") == "option2":
#                 request="book name"
#             elif request.form.get("Author") == "option3":
#                 request="Author"
#             else:
#                 return render_template("error.html", message = "Sorry the details given doesnt match")

#         return render_template("search.html")





