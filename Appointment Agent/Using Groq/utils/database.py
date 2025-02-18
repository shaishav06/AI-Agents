# import sqlite3

# # Database file
# DB_FILE = "appointments.db"

# def create_table():
#     """Create a table to store appointments."""
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS appointments (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT NOT NULL,
#             date TEXT NOT NULL,
#             time TEXT NOT NULL,
#             reason TEXT
#         )
#     """)
#     conn.commit()
#     conn.close()

# def store_appointment(name, email, date, time, reason):
#     """Store an appointment in the database."""
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO appointments (name, email, date, time, reason)
#         VALUES (?, ?, ?, ?, ?)
#     """, (name, email, date, time, reason))
#     conn.commit()
#     conn.close()

# def get_appointments():
#     """Retrieve all scheduled appointments."""
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM appointments")
#     appointments = cursor.fetchall()
#     conn.close()
#     return appointments

# # Run this when the app starts to create the table
# create_table()


import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    """Create the appointments table if it doesn't exist."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        appointment_date TEXT NOT NULL,
        notes TEXT
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def store_appointment(conn, appointment):
    """Insert a new appointment into the appointments table."""
    sql = """
    INSERT INTO appointments (name, email, appointment_date, notes)
    VALUES (?, ?, ?, ?)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, appointment)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error storing appointment: {e}")

def get_appointments(conn):
    """Retrieve all appointments from the appointments table."""
    sql = "SELECT * FROM appointments"
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error retrieving appointments: {e}")
        return []
