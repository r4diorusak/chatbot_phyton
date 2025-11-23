# BigQuery Integration Setup

Bot agent sekarang sudah terintegrasi dengan BigQuery menggunakan **Gemini Function Calling**!

## Cara Kerja

1. User bertanya tentang data/query database
2. Gemini AI mendeteksi perlu query BigQuery
3. Gemini auto-generate SQL query
4. Bot execute query ke BigQuery
5. Hasil dikembalikan ke user dalam bahasa natural

## Setup BigQuery Authentication

### Opsi 1: Application Default Credentials (Recommended)

```bash
# Install gcloud CLI
# Download dari: https://cloud.google.com/sdk/docs/install

# Login
gcloud auth application-default login

# Set project
gcloud config set project YOUR_PROJECT_ID
```

### Opsi 2: Service Account Key

1. Buat Service Account di Google Cloud Console
2. Download JSON key file
3. Update `.env`:

```env
GOOGLE_APPLICATION_CREDENTIALS=C:/path/to/service-account-key.json
GCP_PROJECT_ID=your-project-id
```

4. Tambahkan di `app.py`:

```python
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
```

## Test Query

Setelah setup, coba tanya bot:

- "Show me top 10 rows from dataset.table"
- "Berapa total sales hari ini?"
- "Tampilkan 5 customer dengan revenue tertinggi"

Bot akan otomatis generate query dan tampilkan hasil!

## Troubleshooting

**Error: "BigQuery is not configured"**
- Setup authentication menggunakan salah satu opsi di atas

**Error: "Permission denied"**
- Pastikan service account punya role `BigQuery Data Viewer` atau `BigQuery User`

**Error: "Table not found"**
- Gunakan format lengkap: `project.dataset.table`
