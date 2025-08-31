# Educationpackage.py
import pymysql
from pymysql import Error

def student(host, user, password, database):
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        # The connection has been successfully established at this point.
        # No need for an explicit check like is_connected().
        cursor = connection.cursor()
        name= input("Enter student name: ")
        setup_table_student(cursor, connection,name)
    except Error as e:
        print("Error while connecting to MySQL", e)
        return
def setup_table_student(cursor, connection,name):
    table_name=f"{name}_topics"
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
        topic_id INT AUTO_INCREMENT PRIMARY KEY,
        topic_name VARCHAR(255) NOT NULL,# Name of the topic
        count INT DEFAULT 0, # Number of times the student revised the topic
        last_revised DATE, # Date when the topic was last revised
        next_revision DATE # Date when the topic is due for next revision #based on forgetting curve algorithm
        )''')
    print(f"Table {table_name} is set up successfully.")
    connection.commit()
    choice=topics_menu()
    director(choice,cursor,connection,table_name)
def forgetting_curve(cursor,connection,days):
    """Calculate the next revision date based on the forgetting curve algorithm."""
    # This is a simplified version of the forgetting curve.
    # In a real application, you might want to use a more complex algorithm.
    if days == 0:
        return 1  # Next day
    elif days == 1:
        return 3  # After 3 days
    elif days == 3:
        return 7  # After a week
    elif days == 7:
        return 14 # After two weeks
    elif days == 14:
        return 30 # After a month
    else:
        return days * 2 # Double the interval for longer periods
def topics_menu():
    print("\nTopics Management Menu:")
    print("1. Add Topic")
    print("2. View Topics")
    print("3. Revise Topic ")
    print("4. Back to Main Menu")
    choice = input("Enter your choice: ")
    return choice
def director(choice,cursor,connection,table_name):
    if choice == '1':
        add_topic(cursor,connection,table_name)
    elif choice == '2':
        view_topics(cursor,connection,table_name)
    elif choice == '3':
        revise_topic(cursor,connection,table_name)
    elif choice == '4':
        return
    else:
        print("Invalid choice. Please try again.")
        choice = topics_menu()
        director(choice,cursor,connection,table_name)
def add_topic(cursor,connection,table_name):
    topic_name = input("Topic Name: ")
    
    # Implement the logic to add a topic
    cursor.execute(f"INSERT INTO {table_name} (topic_name) VALUES (%s)", (topic_name,))
    connection.commit() 
    print(f"Topic '{topic_name}' added successfully.")
    opt=topics_menu()
    director(opt,cursor,connection,table_name)
def view_topics(cursor,connection,table_name):
    # Implement the logic to view topics
    cursor.execute(f"SELECT * FROM {table_name}")
    topics = cursor.fetchall()
    print("\nTopics:")
    for topic in topics:
        print(f"ID: {topic[0]}, Name: {topic[1]}, Revisions: {topic[2]}, Last Revised: {topic[3]}, Next Revision: {topic[4]}")
    opt=topics_menu()
    director(opt,cursor,connection,table_name)
def revise_topic(cursor,connection,table_name):
    topic_id = input("Enter the Topic ID to revise: ")
    
    # Fetch the current details of the topic
    cursor.execute(f"SELECT count, last_revised FROM {table_name} WHERE topic_id = %s", (topic_id,))
    result = cursor.fetchone()
    
    if result:
        count, last_revised = result
        count += 1
        
        from datetime import date, timedelta
        today = date.today()
        
        if last_revised:
            last_revised_date = last_revised
            days_since_last_revision = (today - last_revised_date).days
        else:
            days_since_last_revision = 0
        
        next_revision_days = forgetting_curve(cursor,connection,days_since_last_revision)
        next_revision_date = today + timedelta(days=next_revision_days)
        
        # Update the topic details
        cursor.execute(f"""
            UPDATE {table_name}
            SET count = %s, last_revised = %s, next_revision = %s
            WHERE topic_id = %s
        """, (count, today, next_revision_date, topic_id))
        
        connection.commit()
        print(f"Topic ID {topic_id} revised successfully. Next revision on {next_revision_date}.")
    else:
        print("Topic not found.")
    
    opt=topics_menu()
    director(opt,cursor,connection,table_name)