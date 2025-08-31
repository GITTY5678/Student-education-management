
# 🗂️ CLI Event & Study Manager

A **Command-Line Interface (CLI)** tool built with **Python** and **MySQL** to help students organize their **plans, study routines, and daily tasks**.  
Unlike normal task managers, this project integrates a **Forgetting Curve–based study scheduler** to make learning more effective.

---

## ✨ Features

- 👤 **User Management** – create new users or log in as existing users  
- ✅ **Checklist System** – create, view, mark as completed, and auto-update overdue tasks  
- 📅 **Event Manager** – add single or group events with dates  
- 📊 **Auto Status Update** – overdue tasks automatically marked as *incompleted*  
- 🧠 **Forgetting Curve Study Routine** – topics scheduled for revision using spaced repetition  
- 🔐 **Secure Passwords** – stored with `bcrypt` hashing (not plain text)  
- 🖥️ **CLI-First** – lightweight and fast interface  
- 💾 **MySQL Integration** – persistent storage of users, events, and topics  

---

## 🛠️ Installation & Setup

### 1. Clone Repository
'''bash
git clone https://github.com/your-username/cli-study-manager.git
cd cli-study-manager

2. Install Dependencies

Make sure Python 3.x is installed, then install required libraries:

pip install pymysql tabulate tkcalendar bcrypt

3. Setup Database

Run the provided SQL script to initialize the database:

mysql -u root -p < setup.sql


🚀 Usage

Run the main program:

python Student_management.py

Main Menu
Main Menu:
1. New User
2. Existing User
3. Exit

Checklist Menu
Checklist Menu for User 1:
1. Create event
2. View events
3. Mark event as completed
4. GUI Duplicate Events
5. Exit

Topics Management Menu
Topics Management Menu:
1. Add Topic
2. View Topics
3. Revise Topic
4. Back to Main Menu


SCREENSHOTS

<img width="1540" height="163" alt="Main Menu" src="https://github.com/user-attachments/assets/d1440fac-16ef-47a8-bfa8-2f6bdabdab4e" />
<img width="1366" height="176" alt="Checklist menu" src="https://github.com/user-attachments/assets/078c6492-ddc2-417d-af41-0ef85959922b" />
<img width="1366" height="154" alt="Topics Management Menu" src="https://github.com/user-attachments/assets/ce763ecb-187a-48da-a824-d907dd7ab125" />


🧠 Forgetting Curve Integration

This project implements a simplified version of Ebbinghaus’ Forgetting Curve to schedule topic revisions:

1st revision → next day

2nd revision → after 3 days

3rd revision → after 7 days

4th revision → after 14 days

5th revision → after 30 days

Afterwards → interval doubles (e.g., 60 days, 120 days…)

This ensures topics are reviewed just before you’re likely to forget them, maximizing retention.

🚧 Future Scope

📱 GUI/Android version for mobile productivity

🔔 Smart notifications/reminders

✏️ Task editing and advanced search

📊 Analytics dashboard for revision stats

📜 License

This project is open-source and available under the MIT License.


