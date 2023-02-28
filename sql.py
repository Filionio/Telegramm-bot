import sqlite3


async def add(items):
    connect = sqlite3.connect("account.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO users VALUES(?,?,?,?,?)",items)
    connect.commit()
    cursor.close()

async def hist():
    m = []
    connect = sqlite3.connect("account.db")
    cursor = connect.cursor()
    city_find = "SELECT city_find FROM users"
    cursor.execute(city_find)
    data = cursor.fetchall()
    m.append(data)

    arrival_date = "SELECT arrival_date FROM users"
    cursor.execute(arrival_date)
    data = cursor.fetchall()
    m.append(data)

    departure_date = "SELECT departure_date FROM users"
    cursor.execute(departure_date)
    data = cursor.fetchall()
    m.append(data)

    number_people = "SELECT number_people FROM users"
    cursor.execute(number_people)
    data = cursor.fetchall()
    m.append(data)

    offers_screen = "SELECT offers_screen FROM users"
    cursor.execute(offers_screen)
    data = cursor.fetchall()
    m.append(data)

    return m