import sqlite3
from datetime import datetime, timedelta
from typing import List, Optional

class Database:
    def __init__(self, db_name: str = "restaurant.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Таблица столиков
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_number INTEGER UNIQUE NOT NULL,
                capacity INTEGER NOT NULL,
                is_available BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Таблица бронирований
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_id INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                reservation_date TEXT NOT NULL,
                reservation_time TEXT NOT NULL,
                duration_hours INTEGER DEFAULT 2,
                guests_count INTEGER NOT NULL,
                status TEXT DEFAULT 'active',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (table_id) REFERENCES tables (id)
            )
        ''')
        
        # Добавляем тестовые столики
        cursor.execute('''
            INSERT OR IGNORE INTO tables (table_number, capacity) 
            VALUES 
            (1, 2), (2, 2), (3, 4), (4, 4), (5, 6),
            (6, 2), (7, 2), (8, 4), (9, 6), (10, 8)
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)

class Table:
    def __init__(self, table_id, table_number, capacity, is_available):
        self.id = table_id
        self.table_number = table_number
        self.capacity = capacity
        self.is_available = is_available

class Reservation:
    def __init__(self, reservation_id, table_id, customer_name, customer_phone, 
                 reservation_date, reservation_time, duration_hours, guests_count, status):
        self.id = reservation_id
        self.table_id = table_id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.reservation_date = reservation_date
        self.reservation_time = reservation_time
        self.duration_hours = duration_hours
        self.guests_count = guests_count
        self.status = status