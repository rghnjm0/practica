from models import Database, Table, Reservation
from datetime import datetime, timedelta
import sqlite3

class ReservationSystem:
    def __init__(self):
        self.db = Database()
    
    def get_available_tables(self, date: str, time: str, guests: int) -> list[Table]:
        """Получить доступные столики на указанные дату, время и количество гостей"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT t.id, t.table_number, t.capacity, t.is_available
            FROM tables t
            WHERE t.capacity >= ? 
            AND t.is_available = TRUE
            AND t.id NOT IN (
                SELECT r.table_id 
                FROM reservations r 
                WHERE r.reservation_date = ? 
                AND r.reservation_time = ? 
                AND r.status = 'active'
            )
        '''
        
        cursor.execute(query, (guests, date, time))
        results = cursor.fetchall()
        
        tables = []
        for row in results:
            table = Table(row[0], row[1], row[2], row[3])
            tables.append(table)
        
        conn.close()
        return tables
    
    def make_reservation(self, table_id: int, customer_name: str, customer_phone: str,
                        reservation_date: str, reservation_time: str, guests_count: int) -> bool:
        """Создать бронирование"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Проверяем, свободен ли столик
            cursor.execute('''
                SELECT id FROM reservations 
                WHERE table_id = ? 
                AND reservation_date = ? 
                AND reservation_time = ? 
                AND status = 'active'
            ''', (table_id, reservation_date, reservation_time))
            
            if cursor.fetchone():
                return False
            
            # Создаем бронирование
            cursor.execute('''
                INSERT INTO reservations 
                (table_id, customer_name, customer_phone, reservation_date, 
                 reservation_time, guests_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (table_id, customer_name, customer_phone, reservation_date, 
                  reservation_time, guests_count))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error:
            return False
    
    def cancel_reservation(self, reservation_id: int) -> bool:
        """Отменить бронирование"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE reservations 
                SET status = 'cancelled' 
                WHERE id = ?
            ''', (reservation_id,))
            
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
            
        except sqlite3.Error:
            return False
    
    def get_reservations_by_phone(self, phone: str) -> list[Reservation]:
        """Найти бронирования по номеру телефона"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, table_id, customer_name, customer_phone, 
                   reservation_date, reservation_time, duration_hours, 
                   guests_count, status
            FROM reservations 
            WHERE customer_phone = ? 
            AND status = 'active'
            ORDER BY reservation_date, reservation_time
        ''', (phone,))
        
        reservations = []
        for row in cursor.fetchall():
            reservation = Reservation(row[0], row[1], row[2], row[3], row[4], 
                                    row[5], row[6], row[7], row[8])
            reservations.append(reservation)
        
        conn.close()
        return reservations