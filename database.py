import sqlite3

def create_customer_table():
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                      id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      contact_no TEXT NOT NULL,
                      driving_license TEXT NOT NULL,
                      address TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def add_customer(name, contact_no, driving_license, address):
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, contact_no, driving_license, address) VALUES (?, ?, ?, ?)", 
                   (name, contact_no, driving_license, address))
    conn.commit()
    conn.close()

# Example usage:
create_customer_table()
add_customer('John Doe', '987654321', 'XYZ1234', '123 Main St')
