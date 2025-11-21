# Aplikasi Kelayakan Bantuan dengan Fuzzy Logic Mamdani

Aplikasi web berbasis **Flask** untuk menentukan kelayakan bantuan warga menggunakan **Fuzzy Logic Mamdani**. Sistem ini menilai kelayakan berdasarkan tiga parameter utama: penghasilan, jumlah tanggungan, dan jumlah kendaraan.

## 🚀 Fitur
- Login admin (admin/admin123)
- Perhitungan fuzzy berbasis scikit-fuzzy (Mamdani)
- Endpoint API `/calculate` berbasis JSON
- Template HTML terstruktur (login, dashboard, base layout)

## 📂 Struktur Folder
aplikasi/
│ app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── login.html
└── static/

## 🔧 Instalasi Dependensi
pip install flask numpy scikit-fuzzy pandas

## ▶️ Menjalankan Aplikasi
python app.py

Akses aplikasi melalui:
http://127.0.0.1:5000

## 📜 Lisensi
Bebas digunakan untuk pembelajaran dan pengembangan lebih lanjut.
