import smtplib
from datetime import datetime
import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="theater"
)

# Initialize database and create tables if not already present
def setup_database(conn):
    cursor = conn.cursor()
    # Create movies table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        )
    ''')
    # Create bookings table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            movie_id INT NOT NULL,
            tickets INT NOT NULL,
            total_cost DECIMAL(10, 2) NOT NULL,
            booking_time DATETIME NOT NULL,
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        )
    ''')
    conn.commit()

# Initialize database and insert movie data if not already present
def setup_movies(conn):
    cursor = conn.cursor()
    # Check if there are any movies in the table
    cursor.execute('SELECT COUNT(*) FROM movies')
    if cursor.fetchone()[0] == 0:
        movies_data = [("MahaRaja", 700), ("PT SIR", 500), ("Garudan", 600)]
        cursor.executemany('''
            INSERT INTO movies (name, price) VALUES (%s, %s)
        ''', movies_data)
        conn.commit()

# Fetch movies from the database
def fetch_movies(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, price FROM movies')
    movies = cursor.fetchall()
    return movies

# Sending email function
def email_sending(name, email_id,movie_name, ticket, total_cost):
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("bhuvaneshwarial48@gmail.com", "hjji zvzo lmxx rrir")
        subject = "WELCOME TO LAKSHMY THEATER"
        body = f"Hi {name},\nThank you!\n Enjoy the show with your friends and family.\n\nmovie:{movie_name}" 
        now = datetime.now()
        now_dt = now.strftime("%Y-%m-%d %H:%M:%S %p")
        message = f"Subject: {subject}\n\n{body}\n\nBooking time: {now_dt}\n\nTickets: {ticket}\nTotal cost: {total_cost}"
        s.sendmail("bhuvaneshwarial48@gmail.com", email_id, message)
        s.quit()
        print("Mail sent successfully...")
    except Exception as e:
        print(f"Mail not sent: {e}")

# Booking function
def movie_ticket(conn):
    movies = fetch_movies(conn)
    
    print("....LAKSHMY THEATER....")
    print("Movies:")
    for movie in movies:
        print(f"{movie[0]}. {movie[1]} - {movie[2]}")

    name = input("Enter your name: ")
    email_id = input("Enter your email ID: ")
    user_input = int(input("Press any one number: "))

    if user_input < 1 or user_input > len(movies):
        print("Sorry, this movie is not available in the theater.")
        return

    movie_id = user_input
    movie_name = movies[user_input - 1][1]
    ticket = int(input("How many movie tickets do you want? "))
    total_cost = movies[user_input - 1][2] * ticket
    print(f"Total cost for {ticket} tickets to {movie_name}: {total_cost}")

    # Save booking to the database
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO bookings (name, email, movie_id, tickets, total_cost, booking_time)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (name, email_id, movie_id, ticket, total_cost, now))
    conn.commit()

    email_sending(name, email_id,movie_name, ticket, total_cost)

# Set up the database and movies table
setup_database(conn)
setup_movies(conn)

# Book movie tickets
movie_ticket(conn)

# Close the database connection
conn.close()