# tracker/__main__.py
# Titik masuk saat paket dijalankan dengan 'python -m tracker'

import csv
import os

#Impor relatif dari dalam paket 'tracker'
from . import (
    Mahasiswa, 
    RekapKelas,
    build_markdown_report,
    save_text,
    build_html_report #Impor fungsi HTML
)

#impor 'rich'
try:
    from rich import print
    from rich.table import Table
except ImportError:
    print("Modul 'rich' tidak ditemukan, tampilan akan standar.")
    Table = None

#Fungsi Pemuat Data
def load_csv(path):
    """Membaca file CSV dan mengembalikannya sebagai list of dict."""
    try:
        with open(path, encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"[red]Error: File tidak ditemukan di {path}[/red]")
        return []

def bootstrap_from_csv(rekap, att_path="data/attendance.csv", grd_path="data/grades.csv"):
    """
    Memuat data dari file CSV (kehadiran dan nilai)
    dan mengisinya ke dalam objek RekapKelas.
    """
    att = load_csv(att_path)
    grd = load_csv(grd_path)

    if not att or not grd:
        print("[yellow]Data tidak dimuat (file tidak ada atau kosong).[/yellow]")
        return

    # 1. Buat Mahasiswa dari file attendance
    for row in att:
        if "student_id" not in row or "name" not in row:
            print(f"[yellow]Baris data kehadiran tidak valid: {row}[/yellow]")
            continue
        m = Mahasiswa(row["student_id"], row["name"])
        try:
            rekap.tambah_mahasiswa(m)
        except ValueError as e:
            print(f"[yellow]Info: {e}[/yellow]") 

        # 2. Hitung hadir %
        weeks = [k for k in row.keys() if k.startswith("week")]
        if weeks:
            total = len(weeks)
            hadir = 0
            for w in weeks:
                val = row[w].strip()
                if val != "":
                    hadir += int(val)
            
            persen = round(hadir / total * 100.0, 2)
            rekap.set_hadir(m.nim, persen)

    # 3. Isi nilai dari file grades
    by_nim = {g["student_id"]: g for g in grd if "student_id" in g}
    for nim in list(rekap._by_nim.keys()):
        g = by_nim.get(nim)
        if g:
            rekap.set_penilaian(
                nim,
                quiz=float(g.get("quiz", 0) or 0),
                tugas=float(g.get("assignment", 0) or 0),
                uts=float(g.get("mid", 0) or 0),
                uas=float(g.get("final", 0) or 0),
            )
    print("[green]OK, data berhasil dimuat dari CSV.[/green]")


#Fungsi Tampilan & Laporan
def tampilkan_rekap(rows):
    """
    Menampilkan rekap ke terminal menggunakan 'rich.table' jika tersedia.
    
    Args:
        rows (list): List of dict hasil dari rekap.rekap().
    """
    if not rows:
        print("[yellow]Belum ada data untuk ditampilkan.[/yellow]")
        return

    if Table:
        table = Table(title="Rekap Kinerja Mahasiswa")
        table.add_column("NIM")
        table.add_column("Nama")
        table.add_column("Hadir (%)", justify="right")
        table.add_column("Nilai Akhir", justify="right")
        table.add_column("Predikat")
        
        for r in rows:
            table.add_row(
                r['nim'], 
                r['nama'], 
                f"{r['hadir']:.2f}", 
                f"{r['akhir']:.2f}", 
                r['predikat']
            )
        print(table)
    else:
        # Fallback jika 'rich' tidak ada
        print("\n--- REKAP KINERJA ---")
        for r in rows:
            print(f"{r['nim']} | {r['nama']} | Hadir: {r['hadir']:.2f}% | Nilai: {r['akhir']:.2f} | Predikat: {r['predikat']}")

def simpan_laporan(rekap_objek):
    """
    Membuat dan menyimpan laporan Markdown ke folder 'out/'.
    
    Args:
        rekap_objek (RekapKelas): Objek RekapKelas yang berisi data.
    """
    records = rekap_objek.rekap()
    if not records:
        print("[red]Error: Tidak ada data untuk dilaporkan.[/red]")
        return
        
    md_content = build_markdown_report(records)
    
    # Path output sesuai tugas
    output_path = "out/report.md" 
    
    try:
        save_text(output_path, md_content)
        print(f"\n[green]Laporan berhasil disimpan di {output_path}[/green]")
    except IOError as e:
        print(f"[red]Gagal menyimpan laporan: {e}[/red]")

def simpan_laporan_html(rekap_objek):
    """
    Membuat dan menyimpan laporan HTML ke folder 'out/'.
    
    Args:
        rekap_objek (RekapKelas): Objek RekapKelas yang berisi data.
    """
    records = rekap_objek.rekap()
    if not records:
        print("[red]Error: Tidak ada data untuk dilaporkan.[/red]")
        return
        
    html_content = build_html_report(records)
    
    # Path output sesuai tugas
    output_path = "out/report.html" 
    
    try:
        save_text(output_path, html_content)
        print(f"\n[green]Laporan HTML berhasil disimpan di {output_path}[/green]")
    except IOError as e:
        print(f"[red]Gagal menyimpan laporan HTML: {e}[/red]")


#Fungsi Menu Utama

def menu():
    """Menampilkan menu CLI interaktif utama."""
    r = RekapKelas() 
    
    while True:
        # Tampilkan menu
        print("\n=== Student Performance Tracker (Running via -m) ===") 
        print("1) Muat Data dari CSV")
        print("2) Tambah Mahasiswa")
        print("3) Ubah Presensi")
        print("4) Ubah Nilai")
        print("5) Lihat Rekap (Semua)") 
        print("6) Simpan Laporan Markdown")
        print("7) Lihat Remedial")
        print("8) Simpan Laporan HTML")
        print("9) Keluar")
        pilih = input("Pilih: ").strip()

        try:
            if pilih == "1":
                bootstrap_from_csv(r)
            
            elif pilih == "2":
                nim = input("NIM: ").strip()
                nama = input("Nama: ").strip()
                if not nim or not nama:
                    print("[yellow]NIM dan Nama tidak boleh kosong.[/yellow]")
                    continue
                m = Mahasiswa(nim, nama)
                r.tambah_mahasiswa(m)
                print(f"[green]Mahasiswa {nama} ditambah.[/green]")
            
            elif pilih == "3":
                nim = input("NIM: ").strip()
                hadir = float(input("Hadir %: ").strip())
                r.set_hadir(nim, hadir)
                print("[green]Hadir diset.[/green]")
            
            elif pilih == "4":
                nim = input("NIM: ").strip()
                q = float(input("Quiz: ").strip())
                t = float(input("Tugas: ").strip())
                u = float(input("UTS: ").strip())
                a = float(input("UAS: ").strip())
                r.set_penilaian(nim, quiz=q, tugas=t, uts=u, uas=a)
                print("[green]Nilai diset.[/green]")
            
            elif pilih == "5":
                tampilkan_rekap(r.rekap())
            
            elif pilih == "6":
                simpan_laporan(r)
            
            elif pilih == "7":
                print("[yellow]--- Menampilkan Mahasiswa Remedial (Nilai < 70) ---[/yellow]")
                semua_data = r.rekap()
                # Ini logika filter
                data_remedial = [mhs for mhs in semua_data if mhs['akhir'] < 70]
                tampilkan_rekap(data_remedial)
            
            elif pilih == "8":
                simpan_laporan_html(r)

            elif pilih == "9":
                print("Terima kasih telah menggunakan aplikasi ini. Bye.")
                break # Keluar dari loop while
            
            else:
                print("[yellow]Pilihan tidak dikenal. Silakan coba lagi.[/yellow]")
        
        except (ValueError, KeyError, IOError) as e:
            # Tangkap semua error yang mungkin terjadi (mis. validasi nilai, NIM tak ada)
            print(f"\n[red]Terjadi Error: {e}[/red]")
        except Exception as e:
            print(f"\n[red]Terjadi error tak terduga: {e}[/red]")

# Titik masuk utama program KETIKA DIJALANKAN SEBAGAI PAKET
if __name__ == "__main__":
    print("[Info] Menjalankan paket tracker sebagai skrip...")
    menu()

