import psycopg2
import csv
from config import load_config

def execute_query(sql, params=None):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
    except Exception as e:
        print(f'DB error: {e}')

def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook
    (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL
    )
    """
    execute_query(sql)
    print("Table successfully created or already exists.")
def show_all_contacts():
    print("\n=== ALL CONTACTS LIST ===")
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                sql = "SELECT * FROM phonebook ORDER BY id"
                cur.execute(sql)
                rows = cur.fetchall()
                
                if rows:
                    print(f"{'ID':<5} | {'Name':<20} | {'Phone':<15}")
                    print("-" * 45)
                    for row in rows:
                        print(f"{row[0]:<5} | {row[1]:<20} | {row[2]:<15}")
                else:
                    print("The database is currently empty.")
    except Exception as e:
        print(f"Error: {e}")

def insert_data_by_console():
    print("\n=== ADD NEW CONTACT ===")
    name = input("Enter name: ")
    num = input("Enter phone number: ")
    sql = "INSERT INTO phonebook(name, phone_number) VALUES(%s, %s)"
    execute_query(sql, (name, num))
    print("Contact added successfully!")

def insert_data_from_csv(file_path):
    print("\n=== IMPORT FROM CSV ===")
    sql = "INSERT INTO phonebook(name, phone_number) VALUES(%s, %s)"
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row: 
                            cur.execute(sql, row)
        print(f"Data successfully loaded from {file_path}")        
    except Exception as e:
        print(f"Error: {e}")

def update_data():
    print("\n=== UPDATE CONTACT DATA ===")
    print("What would you like to update?")
    print("1 - Phone number")
    print("2 - Contact name")
    choice = input("Select an option (1 or 2): ")

    if choice == '1':
        name = input("Enter the name of the contact to update: ")
        new_phone = input("Enter the new phone number: ")
        sql = "UPDATE phonebook SET phone_number = %s WHERE name = %s"
        execute_query(sql, (new_phone, name))
        print("Phone number updated successfully!")

    elif choice == '2':
        old_name = input("Enter the current name: ")
        new_name = input("Enter the new name for this contact: ")
        sql = "UPDATE phonebook SET name = %s WHERE name = %s"
        execute_query(sql, (new_name, old_name))
        print("Name updated successfully!")
    else:
        print("Invalid selection.")

def search_data():
    print("\n=== SEARCH CONTACTS ===")
    print("Search by:")
    print("1 - Name")
    print("2 - Phone number")
    choice = input("Select an option (1 or 2): ")

    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if choice == '1':
                    search = input("Enter name (or part of it) to search: ")
                    # Using ILIKE for case-insensitive search
                    sql = "SELECT * FROM phonebook WHERE name ILIKE %s"
                    cur.execute(sql, (f'%{search}%',))
                elif choice == '2':
                    search = input("Enter phone number (or part of it) to search: ")
                    sql = "SELECT * FROM phonebook WHERE phone_number LIKE %s"
                    cur.execute(sql, (f'%{search}%',))
                else:
                    print("Invalid selection.")
                    return

                rows = cur.fetchall()
                if rows:
                    print("\nSearch Results:")
                    for row in rows:
                        print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
                else:
                    print("No records found matching your search.")
    except Exception as e:
        print(f"Error: {e}")

def delete():
    print("\n=== DELETE CONTACT ===")
    print("How would you like to delete the contact?")
    print("1 - By Name")
    print("2 - By Phone Number")
    choice = input("Select an option (1 or 2): ")

    if choice == '1':
        name = input("Enter the name to delete: ")
        sql = "DELETE FROM phonebook WHERE name=%s"
        execute_query(sql, (name,))
        print("Contact deleted successfully!")
    elif choice == '2':
        phone = input("Enter the phone number to delete: ")
        sql = "DELETE FROM phonebook WHERE phone_number=%s"
        execute_query(sql, (phone,))
        print("Contact deleted successfully!")
    else:
        print("Invalid selection.")

# === MAIN APPLICATION LOOP ===
if __name__ == "__main__":
    # Ensure the table exists on startup
    create_table()
    
    while True:
        print("1 - Show all contacts")
        print("2 - Add contact manually")
        print("3 - Import contacts from CSV file")
        print("4 - Update contact information")
        print("5 - Search contacts")
        print("6 - Delete a contact")
        print("0 - Exit program")
        
        choice = input()
        
        if choice == '1':
            show_all_contacts()
        elif choice == '2':
            insert_data_by_console()
        elif choice == '3':
            file_name = input("Enter the filename (e.g., phonebook.csv): ")
            insert_data_from_csv(file_name)
        elif choice == '4':
            update_data()
        elif choice == '5':
            search_data()
        elif choice == '6':
            delete()
        elif choice == '0':
            break
        else:
            print("Invalid input")