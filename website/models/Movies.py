from website import db

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column("id", db.Integer, nullable=False, primary_key = True)
    title = db.Column("title", db.String(255), nullable=False)
    category = db.Column("category", db.String(255), nullable=False)
    cast = db.Column("cast", db.String(1800), nullable=False)
    director = db.Column("director", db.String(255), nullable=False)
    producer = db.Column("producer", db.String(255), nullable=False)
    synopsis = db.Column("synopsis", db.String(1800), nullable=False)
    rating = db.Column("rating", db.String(255), nullable=False)
    picture = db.Column("picture", db.String(2048), nullable=False)

    shows = db.relationship("Show", back_populates="movie", order_by="asc(Show.show_date), asc(Show.show_time)")
    reviews = db.relationship("Review", back_populates="movie")

    def __init__(self, title, category, cast, director, producer, synopsis, rating, picture):
        self.title = title
        self.category = category
        self.cast = cast
        self.director = director
        self.producer = producer
        self.synopsis = synopsis
        self.rating = rating
        self.picture = picture

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_category(self):
        return self.category

    def set_category(self, category):
        self.category = category

    def get_cast(self):
        return self.cast

    def set_cast(self, cast):
        self.cast = cast

    def get_director(self):
        return self.director

    def set_director(self, director):
        self.director = director

    def get_producer(self):
        return self.producer

    def set_producer(self, producer):
        self.producer = producer

    def get_synopsis(self):
        return self.synopsis

    def set_synopsis(self, synopsis):
        self.synopsis = synopsis

    def get_rating(self):
        return self.rating

    def set_rating(self, rating):
        self.rating = rating

    def get_picture(self):
        return self.picture

    def set_picture(self, picture):
        self.picture = picture

    def get_shows(self):
        return self.shows

    def get_reviews(self):
        return self.reviews

    def add_review(self, review):
        self.reviews.append(review)

    @staticmethod
    def get_movies():
        return Movie.query.all()