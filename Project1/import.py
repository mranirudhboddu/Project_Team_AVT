import os, csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db.init_app(app)

def main():
    csv_file = open('books.csv')
    reader = csv.reader(csv_file)
    for isbn,title,author,year in reader:
        if isbn == "isbn":
            continue
        else:
            book = books(isbn=isbn, title=title, author=author, year=year)
            db.session.add(book)
            print("Added books with isbn {isbn} and name {title}")
    print("here")
    db.session.commit()


if __name__ == "_main_":
    print(os.getenv("DATABASE_URL"))
    with app.app_context():
        main()