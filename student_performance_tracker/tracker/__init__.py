# tracker/__init__.py

"""
Paket tracker untuk Proyek 2: Student Performance Tracker.

Mengekspor kelas-kelas model (Mahasiswa, Penilaian, RekapKelas)
dan fungsi-fungsi utilitas laporan (build_markdown_report, save_text, letter_grade, build_html_report).
"""

# Impor relatif dari modul-modul 
from .mahasiswa import Mahasiswa
from .penilaian import Penilaian
from .rekap_kelas import RekapKelas
from .report import build_markdown_report, save_text, letter_grade, build_html_report 

# Mendefinisikan __all__ adalah praktik baik untuk paket.
__all__ = [
    'Mahasiswa',
    'Penilaian',
    'RekapKelas',
    'build_markdown_report',
    'save_text',
    'letter_grade',
    'build_html_report' #Tambahkan build_html_report
]

