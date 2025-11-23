# Database Mock - Cara Pakai

## Data yang Tersedia

Bot agent sudah punya **mock database** dengan 3 tabel:

### 1. **customers** - Data pelanggan
- id, name, email, total_orders

### 2. **products** - Data produk
- id, name, price, stock

### 3. **sales** - Data penjualan
- order_id, customer_id, product_id, quantity, total, date

## Cara Query Data via Chat

Tanya bot seperti ini:

```
- "Tampilkan semua customer"
- "Berapa jumlah produk?"
- "Show me all sales data"
- "Siapa customer dengan order terbanyak?"
- "Produk apa yang paling mahal?"
```

Bot akan otomatis query database dan jawab!

## API Endpoints untuk Manage Data

### 1. List Semua Tabel
```bash
GET http://localhost:5000/api/tables
```

### 2. Lihat Data Tabel
```bash
GET http://localhost:5000/api/data/customers
GET http://localhost:5000/api/data/products
GET http://localhost:5000/api/data/sales
```

### 3. Tambah Data Baru

**Tambah Customer:**
```bash
POST http://localhost:5000/api/data/customers
Content-Type: application/json

{
  "id": 6,
  "name": "New Customer",
  "email": "new@example.com",
  "total_orders": 0
}
```

**Tambah Product:**
```bash
POST http://localhost:5000/api/data/products
Content-Type: application/json

{
  "id": 6,
  "name": "Webcam",
  "price": 1200000,
  "stock": 30
}
```

**Tambah Sales:**
```bash
POST http://localhost:5000/api/data/sales
Content-Type: application/json

{
  "order_id": 6,
  "customer_id": 2,
  "product_id": 3,
  "quantity": 1,
  "total": 750000,
  "date": "2025-11-22"
}
```

## Test dengan PowerShell

```powershell
# List tables
Invoke-RestMethod -Uri http://localhost:5000/api/tables

# Get customers
Invoke-RestMethod -Uri http://localhost:5000/api/data/customers

# Add new customer
$body = @{
    id = 6
    name = "Test User"
    email = "test@example.com"
    total_orders = 0
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:5000/api/data/customers -Method POST -Body $body -ContentType "application/json"
```

## Test dengan Browser

Buka di browser:
- http://localhost:5000/api/tables
- http://localhost:5000/api/data/customers
- http://localhost:5000/api/data/products
- http://localhost:5000/api/data/sales

## Upgrade ke BigQuery (Opsional)

Kalau mau pakai BigQuery real:

1. Setup Google Cloud credentials
2. Uncomment BigQuery code di `app.py`
3. Ganti `mock_database` dengan query BigQuery

Untuk sekarang, mock database sudah cukup untuk testing! 🚀
