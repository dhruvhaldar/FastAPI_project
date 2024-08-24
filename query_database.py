import sqlite3

def connect_db():
    return sqlite3.connect('templates.db')

def fetch_all_records():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM templates")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_record(template_id, new_script_type, new_content):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE templates
        SET script_type = ?, content = ?
        WHERE id = ?
    """, (new_script_type, new_content, template_id))
    conn.commit()
    conn.close()

def delete_record(template_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM templates WHERE id = ?", (template_id,))
    conn.commit()
    conn.close()

def add_record(script_type, content):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO templates (script_type, content)
        VALUES (?, ?)
    """, (script_type, content))
    conn.commit()
    conn.close()

def print_all_records():
    print("Current records in the database:")
    records = fetch_all_records()
    for record in records:
        print(record)

def interactive_menu():
    while True:
        print("\nDatabase Management Menu")
        print("1. View all records")
        print("2. Add a new record")
        print("3. Update a record")
        print("4. Delete a record")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            print_all_records()
        elif choice == '2':
            try:
                script_type = input("Enter the script type (python/bash): ").strip()
                content = input("Enter the content for the new template: ").strip()
                add_record(script_type, content)
                print("Record added successfully!")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif choice == '3':
            print_all_records()
            try:
                template_id = int(input("Enter the ID of the record you want to update: ").strip())
                new_script_type = input("Enter the new script type (python/bash): ").strip()
                new_content = input("Enter the new content: ").strip()
                update_record(template_id, new_script_type, new_content)
                print("Record updated successfully!")
            except ValueError:
                print("Invalid input. Please enter a valid ID.")
        elif choice == '4':
            print_all_records()
            try:
                template_id = int(input("Enter the ID of the record you want to delete: ").strip())
                delete_record(template_id)
                print("Record deleted successfully!")
            except ValueError:
                print("Invalid input. Please enter a valid ID.")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    interactive_menu()
