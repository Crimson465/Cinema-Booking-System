from website import db
from enum import Enum

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column("id", db.Integer, primary_key=True)
    rating = db.Column("rating", db.Integer, nullable=False)
    comment = db.Column("comment", db.String(280), nullable=False)

    customer_id = db.Column("customer_id", db.Integer, db.ForeignKey('customers.id'))
    owner = db.relationship("Customer", back_populates="reviews")

    movie_id = db.Column("movie_id", db.Integer, db.ForeignKey('movies.id'))
    movie = db.relationship("Movie", back_populates="reviews")

    def __init__(self, rating, comment):
        self.rating = rating
        self.comment = comment

    def get_rating(self):
        return self.rating

    def get_comment(self):
        return self.comment

    def set_owner(self, owner):
        self.owner = owner

    def set_movie(self, movie):
        self.movie = movie

    @staticmethod
    def get_reviews():
        return Review.query.all()

class Ratings(Enum):
    G = 1
    PG = 2
    PG13 = 3
    R = 4
    X = 5