import pymysql
from datetime import datetime, date
from tabulate import tabulate
from tkinter import *
from tkcalendar import Calendar

# ===== Database Setup =====
def get_db_connection():
    host = input("Enter DB host (default=localhost): ") or "localhost"
    user = input("Enter DB username (default=root): ") or "root"
    password = input("Enter DB password: ")
    database = input("Enter database name: ")

    try:
        con = pymysql.connect(host=host, user=user, password=password, database=database)
        print("✅ Connected to database successfully")
        return con
    except Exception as e:
        print("❌ Connection failed:", e)
        exit(1)

con = get_db_connection()
cur = con.cursor()

def setup_tables():
    cur.execute('''CREATE TABLE IF NOT EXISTS new_users (
        SNO INT PRIMARY KEY,
        name VARCHAR(100),
        password VARCHAR(100)
    )''')
    con.commit()

setup_tables()

# ===== User Management =====
def new_user():
    name = input('Enter name: ')
    password = input('Enter password: ')
    cur.execute("SELECT MAX(SNO) FROM new_users")
    res = cur.fetchone()
    sno = res[0] + 1 if res[0] else 1
    
    # Insert user
    cur.execute("INSERT INTO new_users(SNO, name, password) VALUES (%s, %s, %s)", (sno, name, password))
    con.commit()

    # Create a separate event table for this user
    table_name = f"events_user{sno}"
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        day DATE,
        tasks VARCHAR(255),
        event_status VARCHAR(20) DEFAULT 'pending'
    )''')
    con.commit()

    print(f"✅ User created successfully! Events will be stored in table `{table_name}`")

def existing_user():
    password = input('Enter password: ')
    cur.execute('SELECT SNO, name FROM new_users WHERE password = %s', (password,))
    result = cur.fetchone()
    if result:
        sno, name = result
        print('Welcome,', name)
        checklist(sno)   # pass user ID
    else:
        print('❌ User not found.')

# ===== Checklist Functionalities =====
def checklist(sno):
    table_name = f"events_user{sno}"
    update_past_events(table_name)  # auto-update status
    
    while True:
        print(f'''\nChecklist Menu for User {sno}:
1. Create event
2. View events
3. Mark event as completed
4. GUI Duplicate Events
5. Exit''')
        try:
            choice = int(input('Enter your choice: '))
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            continue

        if choice == 1:
            create_event(table_name)
        elif choice == 2:
            view_events(table_name)
        elif choice == 3:
            mark_completed(table_name)
        elif choice == 4:
            gui_duplicate_events(table_name)
        elif choice == 5:
            break
        else:
            print("❌ Invalid choice. Try again.")

# ===== Event Operations =====
def create_event(table_name):
    try:
        date_str = input('Enter date (yyyy/mm/dd): ')
        event = input('Enter event description: ')
        event_date = datetime.strptime(date_str, "%Y/%m/%d").date()
        cur.execute(f'INSERT INTO {table_name}(day, tasks) VALUES (%s, %s)', (event_date, event))
        con.commit()
        print("✅ Event created successfully!")
    except Exception as e:
        print("❌ Error creating event:", e)

def view_events(table_name):
    cur.execute(f'SELECT day, tasks, event_status FROM {table_name} ORDER BY day')
    data = cur.fetchall()
    if data:
        print(tabulate(data, headers=['Date', 'Task', 'Status'], tablefmt='fancy_grid'))
    else:
        print("ℹ️ No events available.")

def mark_completed(table_name):
    task = input('Enter task to mark as completed: ')
    cur.execute(f'UPDATE {table_name} SET event_status = %s WHERE tasks = %s', ('completed', task))
    if cur.rowcount > 0:
        con.commit()
        print("✅ Task marked as completed!")
    else:
        print("❌ Task not found.")

# ===== Automatic Status Update for Past Events =====
def update_past_events(table_name):
    cur.execute(f'SELECT day, tasks FROM {table_name} WHERE event_status = "pending"')
    for row in cur.fetchall():
        if date.today() > row[0]:
            cur.execute(f'UPDATE {table_name} SET event_status = %s WHERE tasks = %s', ('incompleted', row[1]))
            con.commit()

# ===== GUI-based Event Duplication =====
def gui_duplicate_events(table_name):
    events = []
    selected_dates = []

    def add_event():
        ev = entry_event.get()
        if ev and ev not in events:
            events.append(ev)
            entry_event.delete(0, END)

    def add_date():
        d = cal.get_date()
        if d not in selected_dates:
            selected_dates.append(d)
            display_date_with_delete(d)

    def display_date_with_delete(date):
        row = Frame(list_frame)
        row.pack(anchor='w', pady=2)
        Label(row, text=date, width=15, anchor='w').pack(side=LEFT)
        Button(row, text='🗑️', command=lambda: remove_date(date, row)).pack(side=LEFT, padx=5)

    def remove_date(date, row_widget):
        selected_dates.remove(date)
        row_widget.destroy()

    def save_to_db():
        for d in selected_dates:
            for e in events:
                cur.execute(f'INSERT INTO {table_name}(day, tasks) VALUES (%s, %s)', (d, e))
                con.commit()
        root.destroy()

    root = Tk()
    root.title("Duplicate Events")
    root.geometry("400x550")

    Label(root, text="Enter Event:").pack()
    entry_event = Entry(root)
    entry_event.pack()

    Button(root, text="Add Event", command=add_event).pack()

    cal = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=10)

    Button(root, text="Add Date", command=add_date).pack()

    list_frame = Frame(root)
    list_frame.pack(pady=10)

    Button(root, text="Save", command=save_to_db).pack(pady=10)

    root.mainloop()

# ===== Main Menu =====
def main_menu():
    while True:
        print('''\nMain Menu:
1. New User
2. Existing User
3. Exit''')
        try:
            ch = int(input('Enter your choice: '))
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            continue

        if ch == 1:
            new_user()
        elif ch == 2:
            existing_user()
        elif ch == 3:
            print("👋 Exiting program. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
