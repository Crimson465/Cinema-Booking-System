import sqlite3
from sqlite3 import Error, connect

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    sql_conn = None

    try:
        sql_conn = sqlite3.connect(db_file)
        return sql_conn
    except Error as e:
        print(e)

def run_sql_script(sql_conn, sql_script):
    try:
        cursor = sql_conn.cursor()

        cursor.execute(sql_script)

        sql_conn.close()
    except Error as e:
        print(e)

# Removes promotions Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    DROP TABLE IF EXISTS admins;
""")

# Create admins Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    CREATE TABLE admins(
        id INTEGER PRIMARY KEY NOT NULL,
        password VARCHAR(255) NOT NULL
    );
""")

# Removes promotions Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    DROP TABLE IF EXISTS customers;
""")

# Create customers Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    CREATE TABLE customers(
        id INTEGER PRIMARY KEY NOT NULL,
        password VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        account_state VARCHAR(9) NOT NULL,
        promotion_option INTEGER NOT NULL,
        user_type VARCHAR(255)
    );
""")

# Removes promotions Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    DROP TABLE IF EXISTS payment_cards;
""")

# Create payment_cards Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    CREATE TABLE payment_cards(
        id INTEGER PRIMARY KEY NOT NULL,
        card_number VARCHAR(16) NOT NULL,
        billing_address VARCHAR(255) NOT NULL,
        expiration_date VARCHAR(4) NOT NULL,
        owner_id INTEGER NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES Customers(id)
    );
""")

# Removes promotions Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    DROP TABLE IF EXISTS movies;
""")

# Create movies Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    CREATE TABLE movies(
        id INTEGER PRIMARY KEY NOT NULL,
        title VARCHAR(255) NOT NULL,
        category VARCHAR(255) NOT NULL,
        cast VARCHAR(1800) NOT NULL,
        director VARCHAR(255) NOT NULL,
        producer VARCHAR(255) NOT NULL,
        synopsis VARCHAR(1800) NOT NULL,
        rating VARCHAR(255) NOT NULL,
        state VARCHAR(255) NOT NULL,
        picture VARCHAR(2048) NOT NULL
    );
""")

# Removes reviews Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    DROP TABLE IF EXISTS reviews;
""")

# Create reviews Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    CREATE TABLE reviews(
        id INTEGER PRIMARY KEY NOT NULL,
        rating INTEGER NOT NULL CHECK(rating >= 1 and rating <= 10),
        comment VARCHAR(280) NOT NULL,
        movie_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES Movies(id),
        FOREIGN KEY (customer_id) REFERENCES Customers(id)
    );
""")

# Removes promotions Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    DROP TABLE IF EXISTS theatres;
""")

# Create theatres Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    CREATE TABLE theatres(
        id INTEGER PRIMARY KEY NOT NULL
    );
""")

# Removes promotions Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    DROP TABLE IF EXISTS show_rooms;
""")

# Create show_rooms Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    CREATE TABLE show_rooms(
        id INTEGER PRIMARY KEY NOT NULL,
        room_number INTEGER NOT NULL,
        theatre_id INTEGER NOT NULL,
        FOREIGN KEY (theatre_id) REFERENCES Theatres(id)
    );
""")

# Removes promotions Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    DROP TABLE IF EXISTS shows;
""")

# Create shows Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    CREATE TABLE shows(
        id INTEGER PRIMARY KEY NOT NULL,
        show_date VARCHAR(8) NOT NULL,
        show_time VARCHAR(4) NOT NULL,
        duration VARCHAR(4) NOT NULL,
        movie_id INTEGER NOT NULL,
        show_room_id INTEGER NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES Movies(id),
        FOREIGN KEY (show_room_id) REFERENCES show_rooms(id)
    );
""")

# Removes promotions Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    DROP TABLE IF EXISTS bookings;
""")

# Create bookings Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    CREATE TABLE bookings(
        id INTEGER PRIMARY KEY NOT NULL,
        price_total FLOAT NOT NULL,
        owner_id INTEGER NOT NULL,
        show_id INTEGER NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES Customers(id),
        FOREIGN KEY (show_id) REFERENCES shows(id)
    );
""")

# Removes seats Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    DROP TABLE IF EXISTS seats;
""")

# Create seats Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    CREATE TABLE seats(
        id INTEGER PRIMARY KEY NOT NULL,
        status INTEGER NOT NULL CHECK(status >= 1 and status <= 3),
        seat_number INTEGER NOT NULL,
        show_room_id INTEGER NOT NULL,
        FOREIGN KEY (show_room_id) REFERENCES Show_Rooms(id)
    );
""")

# Removes tickets Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    DROP TABLE IF EXISTS tickets;
""")

# Create tickets Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    CREATE TABLE tickets(
        id INTEGER PRIMARY KEY NOT NULL,
        price FLOAT NOT NULL,
        type VARCHAR(255) NOT NULL,
        booking_id INTEGER NOT NULL,
        promotion_id INTEGER,
        seat_number INTEGER NOT NULL,
        FOREIGN KEY (booking_id) REFERENCES Bookings(id),
        FOREIGN KEY (promotion_id) REFERENCES Promotions(id),
        FOREIGN KEY (seat_number) REFERENCES Seats(seat_number)
    );
""")

# Removes promotions Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    DROP TABLE IF EXISTS promotions;
""")

# Create promotions Table
run_sql_script(create_connection("website/cinema_ebooking_system.db"), """
    CREATE TABLE promotions(
        id INTEGER PRIMARY KEY NOT NULL,
        discount_percent FLOAT NOT NULL CHECK(discount_percent <= 1.0),
        promo_code VARCHAR(255) NOT NULL
    );
""")