# 🤖 AI Bot Agent - Google Gemini

Web application chatbot berbasis Flask yang menggunakan Google Gemini AI API untuk memberikan pengalaman conversational AI yang interaktif.

## ✨ Fitur

- 💬 Chat interface yang modern dan responsif
- 🧠 Powered by Google Gemini AI (gemini-pro)
- 🔄 Contextual conversation dengan memory
- 🎨 UI/UX yang user-friendly
- ⚡ Real-time response
- 🔄 Reset chat history
- 📱 Responsive design

## 🛠️ Teknologi

- **Backend**: Python Flask
- **AI Engine**: Google Generative AI (Gemini)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8 atau lebih tinggi
- Google AI API Key (dapatkan dari [Google AI Studio](https://ai.google.dev/))
- pip (Python package manager)

## 🚀 Instalasi

### 1. Clone atau Download Project

```bash
cd chatbot_phyton
```

### 2. Setup Virtual Environment (Sudah dikonfigurasi)

Virtual environment sudah dibuat secara otomatis di `.venv`

### 3. Install Dependencies (Sudah terinstall)

Dependencies berikut sudah terinstall:
- Flask
- google-generativeai
- python-dotenv

Jika perlu install manual:
```bash
C:/chatbot_phyton/.venv/Scripts/python.exe -m pip install -r requirements.txt
```

### 4. Konfigurasi API Key

API key Google AI sudah dikonfigurasi di file `.env`:
```
GOOGLE_API_KEY=AIzaSyCXqCdwco2ZLcbqS_hABwefTaIsCRPatAw
```

⚠️ **PENTING**: Jangan share API key Anda di repository publik!

## 🎯 Cara Menjalankan

### Jalankan aplikasi:

```bash
C:/chatbot_phyton/.venv/Scripts/python.exe app.py
```

Aplikasi akan berjalan di: **http://localhost:5000**

Buka browser dan akses URL tersebut untuk mulai chat dengan AI bot.

## 📁 Struktur Project

```
chatbot_phyton/
├── .github/
│   └── copilot-instructions.md    # GitHub Copilot instructions
├── .venv/                         # Virtual environment
├── static/
│   ├── style.css                  # Styling aplikasi
│   └── script.js                  # Frontend logic
├── templates/
│   └── index.html                 # Main HTML template
├── .env                           # Environment variables (API key)
├── .env.example                   # Template environment variables
├── .gitignore                     # Git ignore file
├── app.py                         # Main Flask application
├── requirements.txt               # Python dependencies
└── README.md                      # Dokumentasi project
```

## 🔧 API Endpoints

### `GET /`
Menampilkan halaman chat interface

### `POST /api/chat`
Mengirim pesan ke AI bot

**Request body:**
```json
{
  "message": "Halo, apa kabar?"
}
```

**Response:**
```json
{
  "response": "Halo! Saya baik-baik saja, terima kasih. Ada yang bisa saya bantu?",
  "status": "success"
}
```

### `POST /api/reset`
Reset riwayat chat

**Response:**
```json
{
  "status": "success",
  "message": "Chat history reset"
}
```

## 🎨 Fitur UI

- **Modern Gradient Design**: Tampilan dengan gradient ungu yang menarik
- **Smooth Animations**: Animasi slide-in untuk setiap pesan
- **Typing Indicator**: Indikator saat bot sedang mengetik
- **Auto-scroll**: Otomatis scroll ke pesan terbaru
- **Responsive Input**: Textarea yang auto-resize
- **Reset Button**: Tombol untuk menghapus riwayat chat

## 🔐 Keamanan

- API key disimpan di file `.env` (tidak di-commit ke git)
- File `.env` sudah ditambahkan ke `.gitignore`
- Gunakan `.env.example` sebagai template untuk setup

## 🐛 Troubleshooting

### Error: "GOOGLE_API_KEY not found"
- Pastikan file `.env` ada dan berisi API key yang valid
- Cek apakah API key sudah benar

### Error: "Module not found"
- Pastikan semua dependencies terinstall:
  ```bash
  C:/chatbot_phyton/.venv/Scripts/python.exe -m pip install -r requirements.txt
  ```

### Port sudah digunakan
- Ubah port di `app.py`:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)  # Ganti 5000 ke 5001
  ```

## 📝 Pengembangan Lebih Lanjut

Beberapa ide untuk pengembangan:

- [ ] Tambah support untuk upload gambar (gemini-pro-vision)
- [ ] Save chat history ke database
- [ ] Multi-user support dengan authentication
- [ ] Export chat ke PDF
- [ ] Voice input/output
- [ ] Custom AI personality/instructions
- [ ] Streaming response untuk jawaban panjang

## 📄 Lisensi

Project ini dibuat untuk keperluan pembelajaran dan pengembangan.

## �‍💻 Pembuat

- **Nama**: Khairul Adha
- **Email**: r4dioz.88@gmail.com

## �🙏 Credits

- **Google Generative AI**: AI engine
- **Flask**: Web framework
- **Font**: Segoe UI

## 📞 Kontak

Jika ada pertanyaan atau masalah, silakan buat issue di repository ini.

---

**Selamat mencoba! 🚀**
