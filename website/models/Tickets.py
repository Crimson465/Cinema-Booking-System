from website import db

# from Purchase import Booking

class Promotion(db.Model):
    __tablename__ = 'promotions'
    id = db.Column("id", db.Integer, nullable=False, primary_key = True, autoincrement=True)
    discount_percent = db.Column("discount_percent", db.Float, nullable=False)
    promo_code = db.Column("promo_code", db.Integer, nullable=False)

    tickets = db.relationship("Ticket", back_populates="promotion")

    def __init__(self, discount_percent, promo_code):
        self.discount_percent = discount_percent
        self.promo_code = promo_code

    def get_promo(self):
        return self.discount_percent

    def edit_promo(self, percent):
        self.discount_percent = percent

    @staticmethod
    def get_promotions():
        return Promotion.query.all()

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    price = db.Column("price", db.Float, nullable=False)
    type = db.Column("type", db.Integer, nullable=False)

    booking_id = db.Column("booking_id", db.Integer, db.ForeignKey('bookings.id'))
    booking = db.relationship("Booking", back_populates="tickets")

    promotion_id = db.Column("promotion_id", db.Integer, db.ForeignKey('promotions.id'))
    promotion = db.relationship("Promotion", back_populates="tickets")

    seat_number = db.Column("seat_number", db.Integer)
    #seat = db.relationship("Seat", back_populates="tickets")
    def get_price(self):
        return self.price

    def get_type(self):
        return self.type

    def get_seat_number(self):
        return self.seat_number

    def set_price(self):
        match self.type:
            case 'adult':
                self.price = 11.99
            case 'child':
                self.price = 9.69
            case 'senior':
                self.price = 9.89

    def apply_promo(self, promo):
        self.promotion = promo
