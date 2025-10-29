# ==============================================================
# VISUALISASI DISTRIBUSI KELAHIRAN PER KABUPATEN/KOTA (2012–2023)
# Styling: rapi, informatif, mudah dibaca
# ==============================================================

# Import Lib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

# ---------- Styling global ringan ----------
plt.rcParams.update({
    "figure.autolayout": True,
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "grid.linestyle": "--",
    "grid.alpha": 0.35
})

def _fmt_id(x: float) -> str:
    # Format ribuan Indonesia: 1.234.567
    return f"{int(x):,}".replace(",", ".")

# Path dataset
path = "./final_dataset/dataset_kelahiran_jawabarat_2012-2023.csv"

print()
print("----------------------")
print("Proses Pencarian File ")
print("----------------------")
if not os.path.exists(path):
    print(f"- File Tidak Ditemukan : {path}")
else:
    print(f"- File Ditemukan : {path}")

print()
print("----------------------")
print("Proses Membaca File ")
print("----------------------")

try:
    # Membaca dataset
    df = pd.read_csv(path)
    print(f"- Berhasil Membaca File : {path} ✓")

    # Filter tahun 2012–2023
    print()
    print("--------------------------------------------")
    print("Proses Analisis Distribusi Kelahiran Wilayah")
    print("--------------------------------------------")
    df_filter = df[df['tahun'].between(2012, 2023)]
    print(f"- Filter Berdasarkan Tahun ✓")

    # Kelompokkan data berdasarkan kabupaten/kota
    total_per_wilayah = (
        df_filter.groupby('nama_kabupaten_kota')['jumlah_kelahiran']
        .sum()
        .reset_index()
        .sort_values('jumlah_kelahiran', ascending=False)
        .rename(columns={"jumlah_kelahiran": "total_kelahiran"})
    )
    total_all = total_per_wilayah["total_kelahiran"].sum()
    total_per_wilayah["persen"] = (total_per_wilayah["total_kelahiran"] / total_all * 100).round(2)
    print(f"- Mengelompokkan Total Kelahiran per Kabupaten/Kota ✓")

    # Tampilkan 10 wilayah dengan kelahiran tertinggi
    print()
    print("--------------------------------------------------------------")
    print(f"{'Kabupaten/Kota':<30} {'Total Kelahiran':>20}")
    print("--------------------------------------------------------------")
    for _, row in total_per_wilayah.head(10).iterrows():
        print(f"{row['nama_kabupaten_kota']:<30} {int(row['total_kelahiran']):>20,}")

    # Cari wilayah tertinggi & terendah
    kota_max = total_per_wilayah.iloc[0]["nama_kabupaten_kota"]
    kota_min = total_per_wilayah.iloc[-1]["nama_kabupaten_kota"]
    max_val = total_per_wilayah.iloc[0]["total_kelahiran"]
    min_val = total_per_wilayah.iloc[-1]["total_kelahiran"]
    print()
    print(f"- Wilayah dengan Kelahiran Tertinggi : {kota_max} ({max_val:,}) ✓")
    print(f"- Wilayah dengan Kelahiran Terendah  : {kota_min} ({min_val:,}) ✓")

    # -----------------------
    # VISUALISASI DATA
    # -----------------------
    print()
    print("-----------------------")
    print("Proses Visualisasi Data ")
    print("-----------------------")

    fig, ax = plt.subplots(figsize=(12, 8))
    print("- Membuat Canvas Grafik ✓")

    # Highlight Top-N
    TOP_N = 10
    colors = []
    for idx in range(len(total_per_wilayah)):
        if idx < TOP_N:
            colors.append("#2b8fed")   # biru untuk Top-N
        else:
            colors.append("#cfd8dc")   # abu-abu lembut untuk lainnya

    # Plot bar chart horizontal
    bars = ax.barh(
        total_per_wilayah['nama_kabupaten_kota'],
        total_per_wilayah['total_kelahiran'],
        color=colors,
        edgecolor="white",
        linewidth=0.6
    )
    print("- Membuat Diagram Batang Horizontal ✓")

    # Balik urutan agar data tertinggi di atas
    ax.invert_yaxis()
    print("- Mengatur Urutan Wilayah ✓")

    # Judul, subjudul, label sumbu
    ax.set_title("Distribusi Jumlah Kelahiran per Kabupaten/Kota", pad=10)
    ax.set_xlabel("Jumlah Kelahiran (2012–2023)")
    ax.set_ylabel("Kabupaten/Kota")

    # Subjudul (suptitle) & sumber
    # fig.suptitle("Provinsi Jawa Barat • Periode 2012–2023", y=0.98, fontsize=11, fontweight="bold")
    print("- Menambahkan Judul, Subjudul, Label Sumbu ✓")

    # Grid horizontal halus
    ax.grid(axis='x', linestyle='--', alpha=0.35)

    # Format angka sumbu X dengan gaya Indonesia
    ax.xaxis.set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, _: _fmt_id(x))
    )
    print("- Menambahkan Grid Horizontal & Format Angka ✓")

    # Batas sumbu X adaptif (hormati batas 1.500.000 bila perlu)
    data_max = total_per_wilayah['total_kelahiran'].max()
    x_max_auto = data_max * 1.10
    x_cap = 1_500_000  # bisa kamu ubah jika ingin batas tetap
    ax.set_xlim(0, min(x_max_auto, x_cap))

    # Label nilai (angka & %) di ujung batang
    # - Jika batang mepet dengan batas kanan (>= 92% dari xlim), label dipindah ke dalam bar (warna putih)
    x_right = ax.get_xlim()[1]
    for i, (bar, val, pct) in enumerate(zip(bars, total_per_wilayah['total_kelahiran'], total_per_wilayah['persen'])):
        y = bar.get_y() + bar.get_height()/2
        label = f"{_fmt_id(val)} ({pct:.2f}%)"

        # threshold untuk memutuskan posisi label
        if val >= 0.92 * x_right:
            ax.text(val - 0.01 * x_right, y, label, va='center', ha='right',
                    fontsize=9, color="white", fontweight="bold")
        else:
            ax.text(val + 0.008 * x_right, y, label, va='center', ha='left',
                    fontsize=9, color="#37474f")

    print("- Menambahkan Label Nilai & Persentase di Setiap Batang ✓")

    # Legenda kecil untuk highlight
    from matplotlib.patches import Patch
    legend_handles = [
        Patch(facecolor="#2b8fed", edgecolor="white", label=f"Top {TOP_N} tertinggi"),
        Patch(facecolor="#cfd8dc", edgecolor="white", label="Wilayah lainnya")
    ]
    ax.legend(handles=legend_handles, loc="lower right", frameon=False, fontsize=9)

    plt.tight_layout()
    plt.show()
    print("- Visualisasi Berhasil Ditampilkan ✓")

except Exception as e:
    print(f"- Gagal Membaca file : {path} : {e}")
