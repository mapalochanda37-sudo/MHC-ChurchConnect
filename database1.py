import sqlite3
from datetime import datetime
def create_table():
    conn=sqlite3.connect('church.db')
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members(
            id INTEGER PRIMARY KEY AUTOINCREMENT,      
            full_name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            birthday TEXT,
            date_joined TEXT,
            baptised TEXT,
            marital_status TEXT, 
            status TEXT            
        )             
    ''')
    conn.commit()
    conn.close()

def save_member(full_name,phone,email,address,birthday,date_joined,baptised,marital_status,status):
    conn=sqlite3.connect('church.db')
    cursor=conn.cursor()
    cursor.execute('''
        INSERT INTO members (full_name,phone,email,address,birthday,date_joined,baptised,marital_status,status)
        VALUES (?,?,?,?,?,?,?,?,?)
    ''' , (full_name,phone,email,address,birthday,date_joined,baptised,marital_status,status))  
    conn.commit()
    conn.close()

def get_all_members():
    conn = sqlite3.connect("church.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()
    conn.close()
    return rows
             
def search_member(keyword):
    conn = sqlite3.connect("church.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM members
        WHERE full_name LIKE ?
        OR phone LIKE ?
    ''', (f'%{keyword}%', f'%{keyword}%'))
    rows = cursor.fetchall()
    conn.close()
    return rows

def create_transactions_table():
    conn=sqlite3.connect('church.db')
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            amount REAL,
            transaction_type TEXT,
            date TEXT,
            notes TEXT
        )                       
    ''')          
    conn.commit()
    conn.close()
def save_transactions(member_id,amount,transaction_type,date,notes) : 
    conn=sqlite3.connect('church.db')
    cursor=conn.cursor()
    cursor.execute('''
        INSERT INTO transactions(member_id,amount,transaction_type,date,notes)
        VALUES (?,?,?,?,?)
    ''' , (member_id,amount,transaction_type,date,notes))
    conn.commit()
    conn.close()

def get_all_transactions():
    conn=sqlite3.connect('church.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    rows=cursor.fetchall()
    conn.close()
    return rows

def get_member_transactions(member_id):
    conn=sqlite3.connect('church.db')
    cursor=conn.cursor()
    cursor.execute('''
        SELECT * FROM transactions
        WHERE member_id = ?
    ''', (member_id,))
    rows=cursor.fetchall()
    conn.close()
    return rows
def get_total_income_this_month():
    conn=sqlite3.connect('church.db')
    cursor=conn.cursor()
    cursor.execute('''
        SELECT SUM (amount)
        FROM transactions
        WHERE strftime('%Y-%m',date)
        =strftime('%Y-%m','now')
    ''')
    total=cursor.fetchone()[0]
    conn.close()
    return total or 0

def create_events_table():
    conn=sqlite3.connect('church.db')
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT,
            venue TEXT,
            event_date TEXT,
            time TEXT,
            person_in_charge TEXT,
            description TEXT,
            created_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_event(event_name,venue,event_date,event_time,person_in_charge,description):
    conn=sqlite3.connect('church.db')
    cursor=conn.cursor()
    created_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        INSERT INTO events(event_name,venue,event_date,time,person_in_charge,description,created_date)
        VALUES(?,?,?,?,?,?,?)
    ''', (event_name,venue,event_date,event_time,person_in_charge,description,created_date))
    conn.commit()
    conn.close()

def get_all_events():
    conn=sqlite3.connect('church.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM events')
    rows=cursor.fetchall()
    conn.close()
    return rows

def get_upcoming_events():
    conn=sqlite3.connect('church.db')
    cursor=conn.cursor()
    cursor.execute('''
        SELECT * FROM events 
        WHERE event_date >= date('now')
    ''')
    rows=cursor.fetchall()
    return rows

def create_departments_table():
    conn = sqlite3.connect('church.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            chairperson TEXT,
            secretary TEXT,
            treasurer TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_member_departments_table():
    conn = sqlite3.connect('church.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS member_departments(
            member_id INTEGER,
            department_id INTEGER,
            PRIMARY KEY (member_id, department_id)
        )
    ''')
    conn.commit()
    conn.close()

def save_department(name, chairperson, secretary, treasurer):
    conn = sqlite3.connect('church.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO departments(name, chairperson, secretary, treasurer)
        VALUES(?,?,?,?)
    ''', (name, chairperson, secretary, treasurer))
    conn.commit()
    conn.close()

def get_all_departments():
    conn=sqlite3.connect('church.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM departments')
    rows=cursor.fetchall()
    conn.close()
    return rows

def assign_member_to_department(member_id, department_id):
    conn=sqlite3.connect('church.db')
    cursor=conn.cursor()
    cursor.execute('''
        INSERT INTO member_departments(member_id, department_id)
        VALUES (?, ?)
    ''', (member_id, department_id))
    conn.commit()
    conn.close()
def get_department_members(department_id):
    conn = sqlite3.connect('church.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT members.full_name, members.phone
        FROM members
        JOIN member_departments
            ON members.id = member_departments.member_id
        WHERE member_departments.department_id = ?
    ''', (department_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_new_members_this_month():
    conn = sqlite3.connect('church.db')
    cursor = conn.cursor()
    current_month = datetime.now().strftime("%Y-%m")
    cursor.execute('''
        SELECT * FROM members
        WHERE date_joined LIKE ?
    ''', (current_month + '%',))
    rows = cursor.fetchall()
    conn.close()
    return rows

# def reset_all_data():
#     conn = sqlite3.connect('church.db')
#     cursor = conn.cursor()

#     cursor.execute("DELETE FROM member_departments")
#     cursor.execute("DELETE FROM transactions")
#     cursor.execute("DELETE FROM events")
#     cursor.execute("DELETE FROM departments")
#     cursor.execute("DELETE FROM members")

#     cursor.execute("DELETE FROM sqlite_sequence WHERE name='members'")
#     cursor.execute("DELETE FROM sqlite_sequence WHERE name='departments'")
#     cursor.execute("DELETE FROM sqlite_sequence WHERE name='events'")
#     cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")

#     conn.commit()
#     conn.close()
if __name__ == '__main__':
    create_table()
    create_transactions_table()
    print('Database ready!')