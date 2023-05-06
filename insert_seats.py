import sqlite3

conn = sqlite3.connect('website/cinema_ebooking_system.db')

cursor = conn.cursor()


room_num = 1

while(room_num <= 3):
    seat_num = 1
    row_num = 0
    while(seat_num <= 120):
        if(seat_num % 12 == 1):
            row_num += 1
        statement = """INSERT INTO SEATS (status, seat_number, row_number, show_room_id) VALUES (1, {seat_num}, {row_num}, {room_num})""".format(seat_num=seat_num, row_num=row_num, room_num=room_num)

        cursor.execute(statement)
        conn.commit()

        seat_num += 1

    room_num += 1

conn.close()