import sqlite3


class TravelService:
    """A small in-test stub for TravelService with simple DB-backed operations."""
    def __init__(self, service_id=None, title='', price=0.0, max_travelers=0, start_date=None, end_date=None):
        self.service_id = service_id
        self.title = title
        self.price = price
        self.max_travelers = max_travelers
        self.start_date = start_date
        self.end_date = end_date

    def save(self, conn: sqlite3.Connection):
        cur = conn.cursor()
        if self.service_id is None:
            cur.execute("""
            INSERT INTO travel_services (price, rating, destination, flight, hotel, tour, max_travelers, title, description, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.price, 0.0, 'Dest', '', '', '', self.max_travelers, self.title, '', self.start_date, self.end_date))
            conn.commit()
            self.service_id = cur.lastrowid
            return True
        else:
            cur.execute('UPDATE travel_services SET price = ?, max_travelers = ?, title = ?, start_date = ?, end_date = ? WHERE service_id = ?',
                        (self.price, self.max_travelers, self.title, self.start_date, self.end_date, self.service_id))
            conn.commit()
            return True

    def delete(self, conn: sqlite3.Connection):
        if self.service_id is None:
            return False
        cur = conn.cursor()
        cur.execute('DELETE FROM travel_services WHERE service_id = ?', (self.service_id,))
        conn.commit()
        self.service_id = None
        return True

    def remaining_capacity(self, conn: sqlite3.Connection, travel_date: str) -> int:
        if self.service_id is None:
            return 0
        cur = conn.cursor()
        cur.execute("SELECT max_travelers FROM travel_services WHERE service_id = ?", (self.service_id,))
        row = cur.fetchone()
        if not row:
            return 0
        max_tr = row[0] or 0
        cur.execute("SELECT SUM(num_travelers) as total FROM bookings WHERE service_id = ? AND status != 'canceled' AND travel_date = ?",
                    (self.service_id, travel_date))
        booked = cur.fetchone()[0]
        booked = booked or 0
        return max_tr - booked
