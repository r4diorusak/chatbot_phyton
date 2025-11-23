import requests
import json

# URL API
url = "http://localhost:5000/api/data/customers"

# Data customer baru
new_customer = {
    "id": 6,
    "name": "Ahmad Yani",
    "email": "ahmad@example.com",
    "total_orders": 5
}

# Send POST request
response = requests.post(url, json=new_customer)

# Print hasil
print("Status Code:", response.status_code)
print("Response:", response.json())

# Lihat semua customer
all_customers = requests.get(url)
print("\nAll Customers:", all_customers.json())
