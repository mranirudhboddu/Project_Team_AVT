from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Review(db.Model):
    __tablename__ = "review"
    title =db.Column(db.String, primary_key=True)
    username = db.Column(db.String, nullable=False)
    rating = db.Column(db.String, nullable=False)
    review = db.Column(db.String, nullable=False)

    def __init__(self, title, username, rating, review):

        self.title = title
        self.username = username
        self.rating = rating
        self.review = review