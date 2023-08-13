from website import db
from enum import Enum

class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column("id", db.Integer, nullable=False, primary_key = True)
    show_date = db.Column("show_date", db.String(8), nullable=False)
    show_time = db.Column("show_time", db.String(4), nullable=False)
    duration = db.Column("duration", db.String(4), nullable=False)

    bookings = db.relationship("Booking", back_populates="show")

    movie_id = db.Column("movie_id", db.Integer, db.ForeignKey('movies.id'))
    movie = db.relationship("Movie", back_populates="shows")

    show_room_id = db.Column("show_room_id", db.Integer, db.ForeignKey('show_rooms.id'))
    show_room = db.relationship("ShowRoom", back_populates="shows")

    def __init__(self, show_date, show_time, duration):
        self.show_date = show_date
        self.show_time = show_time
        self.duration = duration

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_date(self):
        return self.show_date

    def set_date(self, date):
        self.show_date = date

    def get_time(self):
        return self.show_time

    def set_time(self, time):
        self.show_time = time

    def get_duration(self):
        return self.duration

    def set_duration(self, duration):
        self.duration = duration

    def get_bookings(self):
        return self.bookings

    def get_movie(self):
        return self.movie

    def set_movie(self, movie):
        self.movie = movie

    def get_show_room(self):
        return self.show_room

    def set_show_room(self, show_room):
        self.show_room = show_room

    @staticmethod
    def get_shows():
        return Show.query.all()

class ShowRoom(db.Model):
    __tablename__ = 'show_rooms'
    id = db.Column("id", db.Integer, nullable=False, primary_key = True)
    room_number  = db.Column("room_number", db.Integer, nullable=False)

    shows = db.relationship("Show", back_populates="show_room")

    seats = db.relationship("Seat", back_populates="show_room")

    theater_id = db.Column("theatre_id", db.Integer, db.ForeignKey('theatres.id'))
    theatre = db.relationship("Theatre", back_populates="show_rooms")

    def __init__(self, room_number):
        self.room_number = room_number

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_shows(self):
        return self.shows

    def get_seats(self):
        return self.seats

    def add_seat(self, seat):
        self.seats.append(seat)

    def get_room_number(self):
        return self.room_number

    def set_room_number(self, room_number):
       self.room_number = room_number

    def get_theatre(self):
        return self.theater_id

    @staticmethod
    def get_show_rooms():
        return ShowRoom.query.all()

class Seat(db.Model):
    __tablename__ = 'seats'
    id = db.Column("id", db.Integer, nullable=False, primary_key = True)
    status = db.Column("status", db.Integer, nullable=False)
    number = db.Column("seat_number", db.Integer, nullable=False)
    row_number = db.Column("row_number", db.Integer, nullable=False)

    show_room_id = db.Column("show_room_id", db.Integer, db.ForeignKey('show_rooms.id'))
    show_room = db.relationship("ShowRoom", back_populates="seats")

    # show_id = db.Column("show_id", db.Integer, db.ForeignKey('shows.id'))
    # show = db.relationship("Show", back_populates="seats")


    def __init__(self, number):
        self.status = 'open'
        self.number = number

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_number(self):
        return self.number
    
    def set_number(self, number):
        self.number = number

    @staticmethod
    def get_seats():
        return Seat.query.all()

class Theatre(db.Model):
    __tablename__ = 'theatres'
    id = db.Column("id", db.Integer, nullable=False, primary_key = True)
    show_rooms = db.relationship("ShowRoom", back_populates="theatre")

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_show_rooms(self):
        return self.show_rooms

    def add_show_room(self, show_room):
        self.show_rooms.append(show_room)

    @staticmethod
    def get_theatres():
        return Theatre.query.all()

class SeatStatus(Enum):
    Open = 1
    Occupied = 2
    Selected = 3