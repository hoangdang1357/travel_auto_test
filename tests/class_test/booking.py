import sqlite3
from typing import Optional


class Booking:
    def __init__(self, booking_id: Optional[int] = None, customer_id: Optional[int] = None,
                 service_id: Optional[int] = None, booking_date: Optional[str] = None,
                 travel_date: Optional[str] = None, num_travelers: int = 1,
                 status: str = 'pending', total_amount: float = 0.0):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.service_id = service_id
        self.booking_date = booking_date
        self.travel_date = travel_date
        self.num_travelers = num_travelers
        self.status = status
        self.total_amount = total_amount

    def create(self, conn: sqlite3.Connection):
        cur = conn.cursor()
        # Insert booking with correct parameter order
        cur.execute(
            """INSERT INTO bookings (customer_id, service_id, booking_date, travel_date, num_travelers, status, total_amount)
               VALUES (?, ?, datetime('now'), ?, ?, ?, ?)""",
            (self.customer_id, self.service_id, self.travel_date, self.num_travelers, self.status, self.total_amount),
        )
        conn.commit()
        self.booking_id = cur.lastrowid
        return self.booking_id

    def update(self, conn: sqlite3.Connection, **fields):
        if self.booking_id is None:
            raise ValueError('booking_id is required to update')
        allowed = ['travel_date', 'num_travelers', 'status', 'total_amount']
        updates = []
        params = []
        for k, v in fields.items():
            if k in allowed:
                updates.append(f"{k} = ?")
                params.append(v)
                setattr(self, k, v)
        if not updates:
            return False
        params.append(self.booking_id)
        sql = f"UPDATE bookings SET {', '.join(updates)} WHERE booking_id = ?"
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return True

    def cancel(self, conn: sqlite3.Connection):
        return self.update(conn, status='canceled')

    @classmethod
    def get_by_id(cls, conn: sqlite3.Connection, booking_id: int):
        cur = conn.cursor()
        cur.execute('SELECT * FROM bookings WHERE booking_id = ?', (booking_id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(booking_id=row['booking_id'], customer_id=row['customer_id'], service_id=row['service_id'],
                   booking_date=row['booking_date'], travel_date=row['travel_date'], num_travelers=row['num_travelers'],
                   status=row['status'], total_amount=row['total_amount'])
