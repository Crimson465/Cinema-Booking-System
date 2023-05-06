# Note: use this file for creating routes to pages that do not use
#       any type of authentication process

from flask import Flask, Blueprint, render_template, redirect, url_for, request, session, flash
from . import db, mail
from flask_mail import Mail, Message
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from .models.users import Customer
from .models.Show import Show
from .models.Purchase import PaymentCard
from .models.Movies import Movie
from .models.Show import Show, ShowRoom, Seat
from .models.Purchase import Booking
from .models.Tickets import Ticket, Promotion

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("index.html")


@views.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        return render_template("movies.html", movies=Movie.query.filter(Movie.title.contains(request.form["q"])).filter(Movie.category.contains(request.form["c"])).all())
    else:
        return render_template("movies.html", movies=Movie.query.all())


@views.route('/movies/summary/<int:id>', methods=['GET', 'POST'])
def summary(id):
    if request.method == 'POST':
        return redirect(url_for("views.movies"), code=307)
    else:
        movie = Movie.query.filter_by(id=id).first()
        return render_template("moviesummary.html", movie=movie)


@views.route('/add-movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        try:
            # Get info from request form and add movie to database
            title = request.form["title"]
            category = request.form["category"]
            cast = request.form["cast"]
            director = request.form["director"]
            producer = request.form["producer"]
            synopsis = request.form["synopsis"]
            rating = request.form["rating"]
            picture = request.form["picture"]

            new_movie = Movie(title=title, category=category, cast=cast, director=director,
                              producer=producer, synopsis=synopsis, rating=rating, picture=picture)
            db.session.add(new_movie)
            db.session.commit()
            return redirect(url_for('auth.manage_movies'))
        except:
            flash('Invalid Input', 'warning')
            return redirect(request.url)
    else:
        return render_template("add_movie.html", movie=None)


@views.route('/edit-movie/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):
    if request.method == 'POST':
        # Should get movie using id and perform edit
        movie_id = request.form.get('submit')
        movie = Movie.query.filter_by(id=movie_id).first()
        movie.set_title(request.form['title'])
        movie.set_category(request.form['category'])
        movie.set_cast(request.form['cast'])
        movie.set_director(request.form['director'])
        movie.set_producer(request.form['producer'])
        movie.set_synopsis(request.form['synopsis'])
        movie.set_rating(request.form['rating'])
        movie.set_picture(request.form['picture'])
        db.session.commit()

        return redirect(url_for('auth.manage_movies'))
    else:
        # should get movie and send the movie object to html
        movie = Movie.query.filter_by(id=id).first()
        print(movie)
        return render_template("add_movie.html", movie=movie)


@views.route('/delete-movie', methods=['POST'])
def delete_movie():
    # Should get movie using id and delete it
    movie_id = request.form.get('delete')
    print('movie id: ', movie_id)
    movie = Movie.query.filter_by(id=movie_id).first()
    shows = movie.get_shows()
    for show in shows:
        db.session.delete(show)
    db.session.delete(movie)
    db.session.commit()
    message = f"The movie has been deleted from the database."
    return redirect(url_for('auth.manage_movies'))


@views.route('/add-show', methods=['GET', 'POST'])
def add_show():
    if request.method == 'POST':
        # Get info from request form and add show to database
        print(request.form['show_date'])
        print(request.form['show_time'])
        print(request.form['duration'])
        print(request.form.get('submit'))
        newShow = Show(show_date=request.form['show_date'],
                       show_time=request.form['show_time'], duration=request.form['duration'])
        newShow.movie_id = request.form['movies']
        newShow.show_room_id = request.form['show_rooms']
        db.session.add(newShow)
        db.session.commit()
        # Should get show using id and perform edit
        return redirect(url_for('auth.manage_shows'))
    else:
        show = None
        movies = Movie.get_movies()
        show_rooms = ShowRoom.get_show_rooms()
        return render_template("add_show.html", show=show, movies=movies, show_rooms=show_rooms) #Decorator


@views.route('/edit-show/<int:id>', methods=['GET', 'POST'])
def edit_show(id):
    if request.method == 'POST':
        print(request.form['show_date'])
        print(request.form['show_time'])
        print(request.form['duration'])
        print(request.form.get('submit'))
        show_id = id
        showed = Show.query.filter_by(id=show_id).first()
        db.session.delete(showed)
        newShow = Show(show_date=request.form['show_date'],
                       show_time=request.form['show_time'], duration=request.form['duration'])
        newShow.movie_id = request.form['movies']
        newShow.show_room_id = request.form['show_rooms']
        db.session.add(newShow)
        db.session.commit()
        # Should get show using id and perform edit
        return redirect(url_for('auth.manage_shows'))
    else:
        print('show id: ', id)
        show = Show.query.filter_by(id=id).first()
        movies = Movie.get_movies()
        show_rooms = ShowRoom.get_show_rooms()
        # should get show and send the show object to html
        return render_template("add_show.html", show=show, movies=movies, show_rooms=show_rooms) #Decorator


@views.route('/delete-show/', methods=['POST'])
def delete_show():
    show_id = request.form.get('delete')
    showed = Show.query.filter_by(id=show_id).first()
    db.session.delete(showed)
    db.session.commit()
    print('show id: ', show_id)

    # Should get show using id and delete it
    return redirect(url_for('auth.manage_shows'))


@views.route('/send-promotion/', methods=['POST'])
def send_promotion():
    # Should generate a promo code and email it to all subscribes customers

    return redirect(url_for('auth.manage_promotions'))


@views.route('/profile', methods=['GET', 'POST'])
def profile():
    customer = Customer.query.filter_by(id=str(session["id"])).first()

    firstname = customer.get_first_name()
    lastname = customer.get_last_name()
    email = customer.get_email()
    cards = customer.get_payment_cards()
    promo_opt = customer.get_promo_option()
    payment_cards = customer.get_payment_cards()
    bookings = customer.get_bookings()

    if request.method == 'GET':

        return render_template("Profile.html", firstname=firstname, lastname=lastname, email=email, cards=cards, promo_opt=promo_opt, payment_cards=payment_cards, bookings=bookings)
    else:
        if (not request.form["fname"] == "") or firstname is None:
            customer.set_first_name(request.form["fname"])
        if (not request.form["lname"] == "") or lastname is None:
            lastname = customer.set_last_name(request.form["lname"])

        if (not request.form["Card"] == "" and not request.form["Address"] == "" and not request.form["CardE"] == ""):
            card = PaymentCard(
                card_number=request.form["Card"], billing_address=request.form["Address"], expiration_date=request.form["CardE"])

            customer.add_payment_card(card)

        # promotion = "0"
        promo_result = request.form.get("promo")
        if (promo_result):
            customer.set_promo_option(1)
            promo_opt = 1
        else:
            customer.set_promo_option(0)
            promo_opt = 0

        print('Editing profile')

        db.session.commit()

        return render_template("Profile.html", firstname=firstname, email=email, lastname=lastname, cards=cards, promo_opt=promo_opt, payment_cards=payment_cards)


@views.route('/select-seat/<int:id>', methods=['GET', 'POST'])
def select_seat(id):
    show = Show.query.filter_by(id=id).first()

    if request.method == 'GET':
        return render_template("select_seat.html", show=show)
    else:
        seats = request.form.getlist('seats')
        session['showid'] = id
        session['seats'] = seats
        print("seats: ", seats)
        return redirect(url_for('.buy_tickets'))


@views.route('/buy-tickets', methods=['GET', 'POST'])
def buy_tickets():
    showid = session['showid']
    seats = session['seats']
    show = Show.query.filter_by(id=showid).first()
    print(seats)
    numOfTickets = len(seats)

    if request.method == 'GET':
        print('show: ', show, 'seats: ', seats)
        return render_template("buy_tickets.html", show=show, seats=seats, numOfTickets=numOfTickets)
    else:
        # Note: Need to create Ticket objects from below data
        tickets = request.form.getlist('ticket')
        session['tickets'] = tickets
        return redirect(url_for('.order_summary'))


@views.route('/change-order/<int:id>', methods=['GET', 'POST'])
def change_order(id):
    session['bookingid'] = id
    booking = Booking.query.filter_by(id=id).first()
    return redirect(url_for('.select_seat', id=booking.show_id))

@views.route('/cancel-order/<int:id>', methods=['GET', 'POST'])
def cancel_order(id):
    booking = Booking.query.filter_by(id=id).first()

    if booking != None:
        show = booking.get_show()
        show_room = show.get_show_room()
        seats = show_room.get_seats()
        tickets = booking.get_tickets()
        num_of_tickets = len(tickets)
        
        for i in range(0, num_of_tickets):
            for seat in seats:
                print('ticket seat num: ', tickets[i].get_seat_number())
                print('seat num: ', seat.get_number())
                if int(tickets[i].get_seat_number()) == int(seat.get_id()):
                    seat.set_status(1)
                    break
            

        db.session.delete(booking)
        db.session.commit()
    return redirect(url_for('.profile'))

@views.route('/order-summary', methods=['GET', 'POST'])
def order_summary():
    if request.method == 'GET':
        if not session.get('id') or session['id'] is None: return redirect(url_for('auth.login'))
        id = session['id']
        customer = Customer.query.filter_by(id=id).first()
        show = Show.query.filter_by(id=session['showid']).first()
        print(show)
        seats = session['seats']
        numOfTickets = len(seats)
        tickets = session['tickets']
        print('tickets: ', tickets)

        adultTicketTotal = 0
        childTicketTotal = 0
        seniorTicketTotal = 0

        priceTotal = 0

        for ticket in tickets:
            print('ticket: ', ticket)
            priceTotal += float(ticket)

            match ticket:
                case '11.99':
                    adultTicketTotal += 1
                case '9.69':
                    childTicketTotal += 1
                case '9.89':
                    seniorTicketTotal += 1

        session['priceTotal'] = priceTotal

        return render_template("order_summary.html", customer=customer, show=show, seats=seats, numOfTickets=numOfTickets, tickets=tickets, priceTotal=priceTotal, adultTicketTotal=adultTicketTotal, childTicketTotal=childTicketTotal, seniorTicketTotal=seniorTicketTotal)
    else:
        # Note: Need to create booking with ticket data below
        promo_code = request.form.get('apply_promo')

        if promo_code != '':
            promo = Promotion.query.filter_by(promo_code=promo_code).first()

            if promo == None:
                flash('Promo not found.', 'warning')
                return redirect(url_for('.order_summary'))

            priceTotal = session['priceTotal']
            priceTotal = round(
                priceTotal - (priceTotal * promo.get_promo()), 2)
            session['priceTotal'] = priceTotal

        return redirect(url_for('.order_payment'))


@views.route('/order-payment', methods=['GET', 'POST'])
def order_payment():
    if request.method == 'GET' or session.get('cardnotfound'):
        if session.get('cardnotfound'): session.pop('cardnotfound')
        if not session.get('id') or session['id'] is None: return redirect(url_for('auth.login'))
        id = session['id']
        customer = Customer.query.filter_by(id=id).first()
        payment_cards = customer.get_payment_cards()
        priceTotal = session['priceTotal']
        return render_template("order_payment.html", priceTotal=priceTotal, payment_cards=payment_cards)
    else:
        # Post request for if card info is entered into the form and 'Confirm Purchase' is selected
        # Put needed data in session cookie for Order Confirmation Page
        # Send Confirmation Email
        #flash('No Pre-existing Card Found' + str(session.get('cardnotfound')), 'warning')
        if(session.get('bookingid')):
            booking = Booking.query.filter_by(id=session['bookingid']).first()

            if booking != None:
                show = booking.get_show()
                show_room = show.get_show_room()
                seats = show_room.get_seats()
                tickets = booking.get_tickets()
                num_of_tickets = len(tickets)
        
                for i in range(0, num_of_tickets):
                    for seat in seats:
                        print('ticket seat num: ', tickets[i].get_seat_number())
                        print('seat num: ', seat.get_number())
                        if int(tickets[i].get_seat_number()) == int(seat.get_id()):
                            seat.set_status(1)
                            break
            

                db.session.delete(booking)
                db.session.commit()
            session.pop('bookingid', None)

        if not session.get('id') or session['id'] is None: return redirect(url_for('auth.login'))
        id = session['id']

        tickets = session['tickets']
        customer = Customer.query.filter_by(id=id).first()
        priceTotal = session['priceTotal']
        showid = session['showid']
        seats = session['seats']
        new_booking = Booking(price_total=priceTotal,
                              owner_id=id, show_id=showid)
        db.session.add(new_booking)

        card_number = request.form.get('cardnumber')
        billing_address = request.form.get('address')
        expiration_date = request.form.get(
            'expmonth') + '/' + request.form.get('expyear')

        card = PaymentCard(card_number=card_number,
                           billing_address=billing_address, expiration_date=expiration_date)
        customer.add_payment_card(card)

        show = Show.query.filter_by(id=showid).first()
        show_room = show.get_show_room()

        for i in range(0, len(tickets)):
            s = seats[i]
            ticket = tickets[i]
            seat = Seat.query.filter_by(id=s).first()
            seat.set_status(2)
            type = ""
            match ticket:
                case '11.99':
                    type = "adult"
                case '9.69':
                    type = "child"
                case '9.89':
                    type = "senior"

            new_ticket = Ticket(price=float(
                ticket), type=type, booking_id=new_booking.id, promotion_id=1, seat_number=s)
            db.session.add(new_ticket)
        db.session.commit()

        msg = Message('Order recieved!', sender='cinema.ebooking.llc@gmail.com', recipients = [session['email']])
        msg.body = '''
                    Your order has been placed!
                    Total: {total}
                '''.format(total=priceTotal)
        mail.send(msg)

        return redirect(url_for('.order_confirmation'))


@views.route('/existing-payment', methods=['POST'])
def existing_payment():
    if request.method == 'POST':
        # Post request for if an existing card is chosen and 'Choose Existing' is selected
        # Need to add new nard to customer's card list
        # Put needed data in session cookie for Order Confirmation Page
        # Send Confirmation Email

        id = session['id']

        tickets = session['tickets']
        customer = Customer.query.filter_by(id=id).first()

        card_id = request.form.get('existing-payments')

        if card_id == None:
            session['cardnotfound'] = True
            flash('No Pre-existing Card Found', 'warning')
            return redirect(url_for('.order_payment'))

        if(session.get('bookingid')):
            booking = Booking.query.filter_by(id=session['bookingid']).first()

            if booking != None:
                show = booking.get_show()
                show_room = show.get_show_room()
                seats = show_room.get_seats()
                tickets = booking.get_tickets()
                num_of_tickets = len(tickets)
        
                for i in range(0, num_of_tickets):
                    for seat in seats:
                        print('ticket seat num: ', tickets[i].get_seat_number())
                        print('seat num: ', seat.get_number())
                        if int(tickets[i].get_seat_number()) == int(seat.get_id()):
                            seat.set_status(1)
                            break
            

                db.session.delete(booking)
                db.session.commit()
            session.pop('bookingid', None)

        tickets = session['tickets']
        priceTotal = session['priceTotal']
        showid = session['showid']
        seats = session['seats']

        


        new_booking = Booking(price_total=priceTotal,
                              owner_id=id, show_id=showid)
        db.session.add(new_booking)

        show = Show.query.filter_by(id=showid).first()
        show_room = show.get_show_room()

        for i in range(0, len(tickets)):
            s = seats[i]
            ticket = tickets[i]
            seat = Seat.query.filter_by(id=s).first()
            seat.set_status(2)
            type = ""
            match ticket:
                case '11.99':
                    type = "adult"
                case '9.69':
                    type = "child"
                case '9.89':
                    type = "senior"

            new_ticket = Ticket(price=float(
                ticket), type=type, booking_id=new_booking.id, promotion_id=1, seat_number=s) #factory
            db.session.add(new_ticket)
        db.session.commit()

        msg = Message('Order recieved!', sender='cinema.ebooking.llc@gmail.com', recipients = [session['email']])
        msg.body = '''
                    Your order has been placed!
                    Total: ${total}
                '''.format(total=priceTotal)
        mail.send(msg)

        return redirect(url_for('.order_confirmation'))


@views.route('/order-confirmation', methods=['GET', 'POST'])
def order_confirmation():
    if request.method == 'GET':
        show = Show.query.filter_by(id=session['showid']).first()
        print(show)
        seats = session['seats']
        numOfTickets = len(seats)
        tickets = session['tickets']
        print('tickets: ', tickets)

        adultTicketTotal = 0
        childTicketTotal = 0
        seniorTicketTotal = 0

        priceTotal = session['priceTotal']

        for ticket in tickets:
            print('ticket: ', ticket)

            match ticket:
                case '11.99':
                    adultTicketTotal += 1
                case '9.69':
                    childTicketTotal += 1
                case '9.89':
                    seniorTicketTotal += 1

        flash('Confirmation Email Sent', 'success')
        session.pop('showid', None)
        session.pop('seats', None)
        session.pop('tickets', None)
        session.pop('priceTotal', None)
        return render_template('order_confirmation.html', show=show, seats=seats, numOfTickets=numOfTickets, tickets=tickets, priceTotal=priceTotal, adultTicketTotal=adultTicketTotal, childTicketTotal=childTicketTotal, seniorTicketTotal=seniorTicketTotal)
    else:
        # Need to clear the cookies from the Booking process
        return redirect(url_for('.home'))

@views.route('/delete-card/<int:id>', methods=['GET', 'POST'])
def delete_card(id):
    card = PaymentCard.query.filter_by(id=id).first()

    if card != None:
        db.session.delete(card)
        db.session.commit()
        flash('Card deleted successfully.', 'success')
    else:
        flash('Could not delete card.', 'warning')

    return redirect(url_for('.profile'))