Student Performance Tracker

Program ini adalah aplikasi berbasis terminal (CLI) yang dibuat sebagai submisi Tugas Proyek 2. Aplikasi ini berfungsi untuk memantau performa mahasiswa berdasarkan data kehadiran dan nilai dari file CSV.

Proyek ini disusun dengan menggabungkan konsep OOP dan struktur Paket Modular, serta menyertakan implementasi bonus tantangan.

# Fitur Program

1) Membaca data kehadiran dan nilai dari folder data/ (format CSV)
2) Mengelola data secara object-oriented menggunakan kelas Mahasiswa, Penilaian, dan RekapKelas 
3) Menyediakan menu interaktif untuk menambah, mengubah, dan melihat data.
4) Menampilkan rekap nilai di terminal (mendukung rich untuk tampilan tabel)
5) Menyimpan laporan akhir ke format Markdown di out/report.md
6) [Bonus] Menyaring dan menampilkan mahasiswa yang perlu remedial (nilai < 70) 
7) [Bonus] Mengekspor laporan ke format HTML (out/report.html) dengan warna baris berdasarkan predikat 
8) [Bonus] Dapat dijalankan langsung sebagai paket menggunakan python -m tracker 

# Struktur Proyek

Struktur folder dan file proyek ini mengikuti ketentuan tugas:

student_performance_tracker/
├── app.py              # Titik masuk alternatif
├── README.md           # Dokumentasi proyek ini
├── requirements.txt    # Daftar dependensi (library)
├── .venv/              # Folder virtual environment
├── data/               # Berisi file CSV input
│   ├── attendance.csv
│   └── grades.csv
├── out/                # Folder laporan (dibuat otomatis)
│   ├── report.md
│   └── report.html
└── tracker/            # Paket modular berisi logika program
    ├── __init__.py     # Mengekspor kelas dan fungsi
    ├── __main__.py     # Titik masuk utama (untuk python -m tracker)
    ├── mahasiswa.py    # Kelas Mahasiswa
    ├── penilaian.py    # Kelas Penilaian
    ├── rekap_kelas.py  # Kelas RekapKelas
    └── report.py       # Fungsi untuk membuat laporan MD & HTML


# Instalasi dan Setup
Buka terminal di direktori utama proyek ini.
Buat dan aktifkan virtual environment (direkomendasikan):
# Membuat venv
py -m venv .venv
# Mengaktifkan (PowerShell)
.\.venv\Scripts\Activate.ps1
# Instal semua dependensi yang diperlukan:
pip install -r requirements.txt
# Cara Menjalankan
Setelah instalasi selesai dan virtual environment aktif, Anda bisa menjalankan program dengan salah satu cara berikut:
# Cara 1 (Langsung sebagai Paket - Bonus):
python -m tracker
# Cara 2 (Melalui app.py):
python app.py
# Menu Aplikasi
# Program akan menampilkan menu interaktif:
1) Muat data dari CSV: Membaca file kehadiran & nilai.
2) Tambah mahasiswa: Menambah data mahasiswa baru.
3) Ubah presensi: Mengedit persentase kehadiran.
4) Ubah nilai: Mengubah nilai tugas, kuis, UTS, dan UAS.
5) Lihat rekap (Semua): Menampilkan hasil rekap semua mahasiswa di terminal.
6) Simpan laporan Markdown: Membuat dan menyimpan report.md di folder out/.
7) Lihat remedial (Nilai < 70): Menampilkan mahasiswa dengan nilai akhir di bawah 70.
8) Simpan laporan HTML (Bonus): Membuat dan menyimpan report.html di folder out/.
9) Keluar: Menutup aplikasi.
# Contoh Penggunaan
Alur kerja umum untuk pengujian:
Jalankan program (python -m tracker atau python app.py).
Pilih 1 (Muat data dari CSV).
Pilih 5 (Lihat rekap) untuk melihat tabel di terminal.
Pilih 7 (Lihat remedial) untuk melihat filter.
Pilih 6 (Simpan laporan Markdown).
Pilih 8 (Simpan laporan HTML).
Pilih 9 (Keluar).
Program akan membuat file out/report.md dan out/report.html secara otomatis di dalam folder out/.