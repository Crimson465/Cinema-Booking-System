from website import db

class PaymentCard(db.Model):
    __tablename__ = 'payment_cards'
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    card_number = db.Column("card_number", db.String(16), nullable=False)
    billing_address = db.Column("billing_address", db.String(255), nullable=False)
    expiration_date = db.Column("expiration_date", db.String(4), nullable=False)

    owner_id = db.Column("owner_id", db.Integer, db.ForeignKey('customers.id'))
    owner = db.relationship("Customer", back_populates="payment_cards")

    def __init__(self, card_number, billing_address, expiration_date):
        self.card_number = card_number
        self.billing_address = billing_address
        self.expiration_date = expiration_date

    def get_card_number(self):
        return self.card_number

    def set_card_number(self, card_number):
        self.card_number = card_number

    def get_billing_address(self):
        return self.billing_address

    def set_billing_address(self, billing_address):
        self.billing_address = billing_address

    def get_expiration_date(self):
        return self.expiration_date

    def set_expiration_date(self, expiration_date):
        self.expiration_date = expiration_date

    def get_owner(self):
        return self.owner

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column("id", db.Integer, nullable=False, primary_key=True, autoincrement=True)
    price_total = db.Column("price_total", db.Float, nullable=False)
    
    tickets = db.relationship("Ticket", back_populates="booking", cascade='all, delete-orphan')

    owner_id = db.Column("owner_id", db.Integer, db.ForeignKey('customers.id'))
    owner = db.relationship("Customer", back_populates="bookings")

    show_id = db.Column("show_id", db.Integer, db.ForeignKey('shows.id'))
    show = db.relationship("Show", back_populates="bookings")

    def get_id(self):
        return self.id

    def get_price_total(self):
        return self.price_total

    def get_show(self):
        return self.show

    def set_show(self, show):
        self.show = show

    def get_tickets(self):
        return self.tickets

    def add_ticket(self, ticket):
        self.tickets.append(ticket)
        self.set_total()

    def set_total(self):
        total = 0

        for ticket in self.tickets:
            total += ticket.get_price()

        self.price_total = total

    @staticmethod
    def get_bookings():
        return Booking.query.all()
