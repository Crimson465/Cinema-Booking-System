from website import db
from enum import Enum

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    password = db.Column("password", db.String(255), nullable=False)
    
    def __init__(self, id, password):
        self.id = id
        self.password = password

    def get_id(self):
        return self.id

    def set_id(self, new_id):
        self.id = new_id

    def get_password(self):
        return self.password

    def set_password(self, id, new_password):
        self.password = new_password

    @staticmethod
    def get_admins():
        return Admin.query.all()

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    password = db.Column("password", db.String(255), nullable=False)
    first_name = db.Column("first_name", db.String(255), nullable=False)
    last_name = db.Column("last_name", db.String(255), nullable=False)
    email = db.Column("email", db.String(255), nullable=False)
    account_state = db.Column("account_state", db.String(9), nullable=False)
    promotion_option = db.Column("promotion_option", db.Integer, nullable=False)
    user_type = db.Column("user_type", db.String(255))

    payment_cards = db.relationship("PaymentCard", back_populates="owner", cascade='all, delete-orphan')
    bookings = db.relationship("Booking", back_populates="owner", cascade='all, delete-orphan')
    reviews = db.relationship("Review", back_populates="owner", cascade='all, delete-orphan')

    def __init__(self, password, first_name, last_name, email, account_state, promotion_option, user_type):
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.account_state = account_state
        self.promotion_option = promotion_option
        self.user_type = user_type

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_last_name(self):
        return self.last_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_state(self):
        return self.account_state

    def set_state(self, state):
        self.account_state = state

    def get_user_type(self):
        return self.user_type

    def set_user_type(self, user_type):
        self.user_type = user_type

    def get_promo_option(self):
        return self.promotion_option

    def set_promo_option(self, promo_option):
        self.promotion_option = promo_option

    def get_reviews(self):
        return self.reviews

    def get_payment_cards(self):
        return self.payment_cards

    def add_payment_card(self, card):
        self.payment_cards.append(card)

    def get_bookings(self):
        return self.bookings

    def add_booking(self, booking):
        self.bookings.append(booking)

    def __str__(self):
        return 'first name: ' + self.first_name + ', last name:' + self.last_name

    @staticmethod
    def get_customers():
        return Customer.query.all()

class CustomerStatus(str, Enum):
    Active = 'active'
    Inactive = 'inactive'
    Suspended = 'suspended'