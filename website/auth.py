# Note: use this file for creating routes to pages that use some 
#       type of authentication or encryption
from http import server
from sre_constants import SUCCESS
import time
import sqlite3
import traceback
import os
import random

from .models.Tickets import Promotion
from flask_mail import Mail, Message
from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash, session

from flask import Flask, Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, mail
from .models.users import Customer
from .models.Show import Show
from .models.Movies import Movie
from .models.Tickets import Ticket, Promotion

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            customer = Customer.query.filter_by(email=email).first()
        except:
            error = "Incorrect email or password, or you haven't activated your account"
            traceback.print_exc()
            return render_template("login.html", error=error)

        if check_password_hash(customer.get_password(), password) and (customer.get_state() == 'active'):
            session["email"] = customer.get_email()
            session["id"] = customer.get_id()
            session["admin"] = customer.get_user_type() == "admin"
            print('user is admin?: ', customer.get_user_type())
            if session.get('tickets'): return redirect(url_for('views.order_summary'))
            return redirect(url_for('views.movies'))
        else:
            error = "Incorrect email or password, or you haven't activated your account"
    return render_template("login.html", error=error)

@auth.route('/register', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            name = request.form["name"]
            name = name.split(' ')
            first_name = name[0]
            last_name = name[1]
            email = request.form['email']
            password = request.form['password']
            confirm = request.form["password_confirm"]
            promotion_verifier = request.form.getlist("promotion_verifier")
            promotion_option = 0

            email_exists_result = len(Customer.query.filter_by(email=email).all())

            if email_exists_result != 0:
                flash("Email already in use. Please login.", 'warning')
                return redirect(url_for('auth.login'))

            if 'on' in promotion_verifier:
                promotion_option = 1

            if password == confirm:

                new_customer = Customer(password=generate_password_hash(password, method="sha256"), first_name=first_name, last_name=last_name, email=email, account_state='inactive', promotion_option=promotion_option, user_type='customer')
                db.session.add(new_customer)
                db.session.commit()

                msg = Message('Account creation successful!', sender='cinema.ebooking.llc@gmail.com', recipients = [email])
                msg.body = '''
                    Your account has been created successfully

                    Confirmation Link: http://127.0.0.1:5000/confirm-registration/{id}
                    Verification Code: dhnxfgzdfS
                '''.format(id=new_customer.id)
                mail.send(msg)

                flash('Signup Successful', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Invalid Input', 'warning')
                return redirect(request.url)
        except:
            flash('Invalid Input', 'warning')
            traceback.print_exc()
            return redirect(request.url)
    else:
        return render_template("register.html")

@auth.route('/confirm-registration/<usrid>')
def confirm_registration(usrid):
    try:
        customer = Customer.query.filter_by(id=usrid).first()
    except:
        flash('Invalid Input', 'warning')
        traceback.print_exc()
        return redirect(url_for('auth.login'))

    print('user {id} account state: {account_state}'.format(id=customer.get_id(), account_state=customer.get_state()))

    if customer.get_state() == 'inactive':
        customer.set_state('active')
        db.session.commit()

        flash("Account has been verified", 'success')
        return redirect(url_for('auth.login'))
    elif customer.get_state() == 'active':
        flash("Account already verified", 'success')
        return redirect(url_for('auth.login'))
    else:
        flash("Error verifying account", 'warning')
        return redirect(url_for('auth.login'))

@auth.route('/admin-panel')
def admin_panel():
    return render_template("admin-panel.html")

@auth.route('/logout')
def logout():
    session["email"] = None
    session["id"] = None
    session["admin"] = False
    session.pop('tickets', None)
    return render_template("index.html")

@auth.route('/manage-movies', methods = ['GET', 'POST'])
def manage_movies():
    movies = Movie.get_movies()

    return render_template("manage-movies.html", movies=movies)

@auth.route('/manage-shows')
def manage_shows():
    shows = Show.get_shows()

    return render_template("manage-shows.html", shows=shows)

@auth.route('/manage-promotions', methods = ['GET', 'POST'])
def manage_promotions():
    if request.method == 'POST':
        promotion = request.form['promotion']
        promoCode = str(random.randint(1000, 9999))

        promoCustomers = Customer.query.filter_by(promotion_option=1)
        for customer in promoCustomers:
            msg = Message('New Promo Code Available!', sender='cinema.ebooking.llc@gmail.com', recipients = [customer.email])
            msg.body = '''
                        There is a new promo code available to you for {percent}% off any movie!

                        Here is your promo code: {promoCode}
                    '''.format(percent=promotion,promoCode=promoCode)
            mail.send(msg)
        
        flash('Promotion Emails Successful', 'success')

        promo = Promotion(discount_percent=float(promotion)*0.01, promo_code=promoCode)
        db.session.add(promo)
        db.session.commit()
        return render_template("manage-promotions.html")
    else:
        return render_template("manage-promotions.html")

@auth.route('/editpassword/<usrid>', methods = ['GET', 'POST'])
def edit_password(usrid):
    if request.method == 'POST':
        try:
            password = request.form['password']

            customer = Customer.query.filter_by(id=usrid).first()
            customer.set_password(generate_password_hash(password, method="sha256"))
            db.session.commit()

            flash('Password Change Successful', 'success')
            return redirect(url_for('auth.login'))
        except:
            flash('Invalid Input', 'warning')
            traceback.print_exc()
            return redirect(request.url)
    else:
        return render_template("editpassword.html")

@auth.route('/forgotpassword', methods = ['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        try:
            email = request.form['email']

            customer = Customer.query.filter_by(email=email).first()
            id = customer.get_id()

            msg = Message('Forgot Password', sender='cinema.ebooking.llc@gmail.com', recipients = [email])
            msg.body = '''
                Here is a password recovery link

                Forgot Password Link: http://127.0.0.1:5000/editpassword/{id}
            '''.format(id=id)
            mail.send(msg)

            # flash('Signup Successful', 'success')
            return redirect(url_for('auth.edit_password'))
        except:
            flash('Invalid Input', 'warning')
            traceback.print_exc()
            return redirect(request.url)
    else:
        return render_template("forgotpassword.html")