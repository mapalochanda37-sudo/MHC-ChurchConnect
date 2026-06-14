import psycopg2
from psycopg2 import pool
from datetime import datetime
import streamlit as st

DATABASE_URL = st.secrets["DATABASE_URL"]

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members(
            id SERIAL PRIMARY KEY,
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

def save_member(full_name, phone, email, address, birthday, date_joined, baptised, marital_status, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO members(full_name, phone, email, address, birthday, date_joined, baptised, marital_status, status)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (full_name, phone, email, address, birthday, date_joined, baptised, marital_status, status))
    conn.commit()
    conn.close()

def get_all_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM members')
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_member(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM members
        WHERE full_name ILIKE %s
        OR phone ILIKE %s
    ''', (f'%{keyword}%', f'%{keyword}%'))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_member_by_id(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM members WHERE id = %s', (member_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_member_status(member_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE members SET status = %s WHERE id = %s
    ''', (status, member_id))
    conn.commit()
    conn.close()

def create_transactions_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions(
            id SERIAL PRIMARY KEY,
            member_id INTEGER,
            amount REAL,
            transaction_type TEXT,
            date TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_transactions(member_id, amount, transaction_type, date, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions(member_id, amount, transaction_type, date, notes)
        VALUES(%s, %s, %s, %s, %s)
    ''', (member_id, amount, transaction_type, date, notes))
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_member_transactions(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM transactions
        WHERE member_id = %s
    ''', (member_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_total_income_this_month():
    conn = get_connection()
    cursor = conn.cursor()
    current_month = datetime.now().strftime("%Y-%m")
    cursor.execute('''
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE date LIKE %s
    ''', (current_month + '%',))
    total = cursor.fetchone()[0]
    conn.close()
    return total

def create_events_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events(
            id SERIAL PRIMARY KEY,
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

def save_event(event_name, venue, event_date, event_time, person_in_charge, description):
    conn = get_connection()
    cursor = conn.cursor()
    created_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        INSERT INTO events(event_name, venue, event_date, time, person_in_charge, description, created_date)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
    ''', (event_name, venue, event_date, event_time, person_in_charge, description, created_date))
    conn.commit()
    conn.close()

def get_all_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_upcoming_events():
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        SELECT * FROM events
        WHERE event_date >= %s
    ''', (today,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def create_departments_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments(
            id SERIAL PRIMARY KEY,
            name TEXT,
            chairperson TEXT,
            secretary TEXT,
            treasurer TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_member_departments_table():
    conn = get_connection()
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO departments(name, chairperson, secretary, treasurer)
        VALUES(%s, %s, %s, %s)
    ''', (name, chairperson, secretary, treasurer))
    conn.commit()
    conn.close()

def get_all_departments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM departments')
    rows = cursor.fetchall()
    conn.close()
    return rows

def assign_member_to_department(member_id, department_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO member_departments(member_id, department_id)
        VALUES(%s, %s)
    ''', (member_id, department_id))
    conn.commit()
    conn.close()

def get_department_members(department_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT members.full_name, members.phone
        FROM members
        JOIN member_departments
            ON members.id = member_departments.member_id
        WHERE member_departments.department_id = %s
    ''', (department_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_new_members_this_month():
    conn = get_connection()
    cursor = conn.cursor()
    current_month = datetime.now().strftime("%Y-%m")
    cursor.execute('''
        SELECT * FROM members
        WHERE date_joined LIKE %s
    ''', (current_month + '%',))
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == '__main__':
    create_table()
    create_transactions_table()
    print('Database ready!')