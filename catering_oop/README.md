# Sistem Pemesanan Katering — Python OOP

Aplikasi web sederhana dengan frontend HTML/CSS, backend Flask, dan database SQLite.

## Menjalankan aplikasi

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Buka `http://127.0.0.1:5000` di browser. Database `catering.db` dibuat otomatis.

## Konsep OOP

- Atribut & method: seluruh class pada `models.py`.
- Encapsulation: atribut `Person.__name` dan `Person.__phone` dengan property setter.
- Inheritance: `Customer` dan `Chef` mewarisi `Person`; `RegularCustomer` dan `PromoCustomer` mewarisi `Customer`.
- Polymorphism: implementasi berbeda `calculate_bill()` untuk pelanggan reguler dan promo.
- Abstraction: abstract class `Person`/`Customer` dan `CateringService` sebagai lapisan layanan.
- Association/composition: `Order` memiliki `Customer` dan daftar `OrderItem`.

## Struktur

`app.py` route web · `models.py` domain OOP · `services.py` logika bisnis · `database.py` SQLite/repository · `templates/` frontend · `static/` CSS · `tests/` pengujian.
