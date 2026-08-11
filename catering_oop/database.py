import sqlite3
from pathlib import Path


class Database:
    """Encapsulates all low-level SQLite operations."""

    def __init__(self, path: str):
        self.__path = Path(path)

    def connect(self):
        connection = sqlite3.connect(self.__path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self):
        schema = """
        CREATE TABLE IF NOT EXISTS menus (
          id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
          category TEXT NOT NULL CHECK(category IN ('Makanan','Minuman','Snack')),
          price INTEGER NOT NULL CHECK(price >= 0), stock INTEGER NOT NULL CHECK(stock >= 0)
        );
        CREATE TABLE IF NOT EXISTS customers (
          id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone TEXT NOT NULL,
          address TEXT NOT NULL, customer_type TEXT NOT NULL CHECK(customer_type IN ('regular','promo'))
        );
        CREATE TABLE IF NOT EXISTS orders (
          id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL,
          delivery_date TEXT NOT NULL, payment_method TEXT NOT NULL, notes TEXT,
          subtotal INTEGER NOT NULL, discount INTEGER NOT NULL, total INTEGER NOT NULL,
          status TEXT NOT NULL DEFAULT 'Baru', created_at TEXT NOT NULL,
          FOREIGN KEY(customer_id) REFERENCES customers(id)
        );
        CREATE TABLE IF NOT EXISTS order_items (
          id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER NOT NULL, menu_id INTEGER NOT NULL,
          menu_name TEXT NOT NULL, price INTEGER NOT NULL, quantity INTEGER NOT NULL,
          FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE,
          FOREIGN KEY(menu_id) REFERENCES menus(id)
        );
        """
        with self.connect() as conn:
            conn.executescript(schema)
            count = conn.execute("SELECT COUNT(*) FROM menus").fetchone()[0]
            if count == 0:
                conn.executemany(
                    "INSERT INTO menus(name,category,price,stock) VALUES(?,?,?,?)",
                    [("Nasi Ayam Bakar", "Makanan", 28000, 100),
                     ("Nasi Rendang", "Makanan", 32000, 80),
                     ("Es Teh Lemon", "Minuman", 8000, 120),
                     ("Puding Cokelat", "Snack", 10000, 60)],
                )


class CateringRepository:
    def __init__(self, database: Database):
        self.db = database

    def all_menus(self):
        with self.db.connect() as conn:
            return conn.execute("SELECT * FROM menus ORDER BY category,name").fetchall()

    def save_menu(self, name, category, price, stock):
        with self.db.connect() as conn:
            conn.execute("INSERT INTO menus(name,category,price,stock) VALUES(?,?,?,?)",
                         (name, category, price, stock))

    def delete_menu(self, menu_id):
        with self.db.connect() as conn:
            used = conn.execute("SELECT 1 FROM order_items WHERE menu_id=? LIMIT 1", (menu_id,)).fetchone()
            if used:
                raise ValueError("Menu sudah dipakai dalam transaksi dan tidak dapat dihapus.")
            conn.execute("DELETE FROM menus WHERE id=?", (menu_id,))

    def all_customers(self):
        with self.db.connect() as conn:
            return conn.execute("SELECT * FROM customers ORDER BY id DESC").fetchall()

    def save_customer(self, customer):
        with self.db.connect() as conn:
            cursor = conn.execute(
                "INSERT INTO customers(name,phone,address,customer_type) VALUES(?,?,?,?)",
                (customer.name, customer.phone, customer.address, customer.customer_type),
            )
            return cursor.lastrowid

    def customer_by_id(self, customer_id):
        with self.db.connect() as conn:
            return conn.execute("SELECT * FROM customers WHERE id=?", (customer_id,)).fetchone()

    def save_order(self, customer_id, order):
        with self.db.connect() as conn:
            cursor = conn.execute(
                """INSERT INTO orders(customer_id,delivery_date,payment_method,notes,subtotal,
                   discount,total,created_at) VALUES(?,?,?,?,?,?,?,?)""",
                (customer_id, order.delivery_date, order.payment_method, order.notes,
                 order.subtotal, order.discount, order.total, order.created_at.isoformat()),
            )
            order_id = cursor.lastrowid
            for item in order.items:
                conn.execute("""INSERT INTO order_items(order_id,menu_id,menu_name,price,quantity)
                             VALUES(?,?,?,?,?)""",
                             (order_id, item.menu_id, item.menu_name, item.price, item.quantity))
                updated = conn.execute("UPDATE menus SET stock=stock-? WHERE id=? AND stock>=?",
                                       (item.quantity, item.menu_id, item.quantity))
                if updated.rowcount == 0:
                    raise ValueError(f"Stok {item.menu_name} tidak mencukupi.")
            return order_id

    def all_orders(self):
        with self.db.connect() as conn:
            return conn.execute("""SELECT o.*, c.name customer_name FROM orders o
              JOIN customers c ON c.id=o.customer_id ORDER BY o.id DESC""").fetchall()

    def update_status(self, order_id, status):
        if status not in {"Baru", "Diproses", "Selesai", "Dibatalkan"}:
            raise ValueError("Status tidak valid.")
        with self.db.connect() as conn:
            conn.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))

    def dashboard(self):
        with self.db.connect() as conn:
            return conn.execute("""SELECT (SELECT COUNT(*) FROM menus) menus,
              (SELECT COUNT(*) FROM customers) customers,
              (SELECT COUNT(*) FROM orders) orders,
              COALESCE((SELECT SUM(total) FROM orders WHERE status!='Dibatalkan'),0) revenue""").fetchone()
