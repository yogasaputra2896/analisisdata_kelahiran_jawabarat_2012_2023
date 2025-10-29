# ====================================================================
# VISUALISASI KELAHIRAN BERDASARKAN JENIS KELAMIN & STATUS (2012–2023)
# ====================================================================

# Import Library
import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------
# Konfigurasi tampilan global (ringan)
# -------------------------
plt.rcParams.update({
    "figure.autolayout": True,
    "axes.titlesize": 13,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9
})

def _fmt_thousands(x: float) -> str:
    # Format 1.234.567 (style Indonesia)
    return f"{int(x):,}".replace(",", ".")

def _legend_triplet(name: str, value: float, percent: float) -> str:
    return f"{name}  •  {_fmt_thousands(value)}  •  {percent:.2f}%"

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

# Membaca file
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
    print("-----------------------------------------------")
    print("Proses Analisis Berdasarkan Jenis dan Status")
    print("-----------------------------------------------")
    df_filter = df[df['tahun'].between(2012, 2023)].copy()
    print(f"- Filter Berdasarkan Tahun ✓")

    # ==================================================
    # BAGIAN 1: ANALISIS BERDASARKAN JENIS KELAMIN
    # ==================================================
    print()
    print("-----------------------------------")
    print("Analisis Berdasarkan Jenis Kelamin")
    print("-----------------------------------")

    # Kelompokkan & urutkan (kecil → besar agar visual terbaca)
    total_jenis_kelamin = (
        df_filter.groupby('jenis_kelamin', as_index=False)['jumlah_kelahiran']
        .sum()
        .sort_values('jumlah_kelahiran', ascending=True)
    )
    print(f"- Mengelompokkan Total Berdasarkan Jenis Kelamin ✓")

    # Menampilkan hasil kelompok
    print()
    print(f"{'Jenis Kelamin':<15} {'Jumlah Kelahiran':>20}")
    print("-----------------------------------------------")
    for _, row in total_jenis_kelamin.iterrows():
        print(f"{row['jenis_kelamin']:<15} {int(row['jumlah_kelahiran']):>20,}")

    # -----------------
    # VISUALISASI DATA 
    # -----------------
    print()
    print("-------------------------------------")
    print("Proses Visualisasi Data Jenis Kelamin (Donut)")
    print("-------------------------------------")

    fig, ax = plt.subplots(figsize=(7.4, 7.4))
    print("- Membuat Canvas Donut Chart ✓")

    total_all = total_jenis_kelamin['jumlah_kelahiran'].sum()
    colors_gender = ['#f759ad', '#2b8fed']

    wedges, _texts, autotexts = ax.pie(
        total_jenis_kelamin['jumlah_kelahiran'],
        labels=None,                
        startangle=90,
        autopct=lambda p: f"{p:.2f}%",
        pctdistance=0.78,
        colors=colors_gender,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1, 'width': 0.45}
    )

    # Styling % di dalam cincin
    for at in autotexts:
        at.set_fontsize(10)
        at.set_color("white")
        at.set_weight("bold")

    # Legend: Nama • Jumlah • %
    percents_gender = total_jenis_kelamin["jumlah_kelahiran"] / total_all * 100
    legend_labels = [
        _legend_triplet(name, val, pct)
        for name, val, pct in zip(
            total_jenis_kelamin["jenis_kelamin"],
            total_jenis_kelamin["jumlah_kelahiran"],
            percents_gender
        )
    ]

    ax.legend(
        wedges,
        legend_labels,
        title="Keterangan",
        loc="lower center",
        bbox_to_anchor=(0.5, -0.1),
        frameon=False,
        borderaxespad=0.8
    )

    # Teks tengah donut (dua baris)
    ax.text(0, 0.06, "TOTAL", ha="center", va="center", fontsize=9, color="#666666")
    ax.text(0, -0.05, _fmt_thousands(total_all), ha="center", va="center",
            fontsize=14, fontweight="bold")

    # Judul + subjudul
    ax.set_title("Proporsi Kelahiran berdasarkan Jenis Kelamin")
    ax.set_aspect('equal')

    plt.show()
    print("- Visualisasi Jenis Kelamin (Donut) Berhasil Ditampilkan ✓")


    # ==================================================
    # BAGIAN 2: ANALISIS BERDASARKAN STATUS KELAHIRAN
    # ==================================================
    print()
    print("-----------------------------------------------")
    print("Analisis Berdasarkan Status Kelahiran")
    print("-----------------------------------------------")

    total_status = (
        df_filter.groupby('status_kelahiran', as_index=False)['jumlah_kelahiran']
        .sum()
        .sort_values('jumlah_kelahiran', ascending=True)
    )
    print(f"- Mengelompokkan Total Berdasarkan Status Kelahiran ✓")

    # Menampilkan hasil kelompok
    print()
    print(f"{'Status Kelahiran':<20} {'Jumlah Kelahiran':>20}")
    print("-----------------------------------------------")
    for _, row in total_status.iterrows():
        print(f"{row['status_kelahiran']:<20} {int(row['jumlah_kelahiran']):>20,}")

    # -----------------------
    # VISUALISASI DATA 
    # -----------------------
    print()
    print("------------------------------------------")
    print("Proses Visualisasi Data Status Kelahiran (Donut)")
    print("------------------------------------------")

    fig, ax = plt.subplots(figsize=(7.4, 7.4))
    print("- Membuat Canvas Donut Chart ✓")

    total_all_status = total_status['jumlah_kelahiran'].sum()
    colors_status = ['#e15759', '#59a14f'] 

    wedges, _texts, autotexts = ax.pie(
        total_status['jumlah_kelahiran'],
        labels=None,
        startangle=90,
        autopct=lambda p: f"{p:.2f}%",
        pctdistance=0.78,
        colors=colors_status,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1, 'width': 0.45}
    )

    for at in autotexts:
        at.set_fontsize(10)
        at.set_color("white")
        at.set_weight("bold")

    percents_status = total_status["jumlah_kelahiran"] / total_all_status * 100
    legend_labels = [
        _legend_triplet(name, val, pct)
        for name, val, pct in zip(
            total_status["status_kelahiran"],
            total_status["jumlah_kelahiran"],
            percents_status
        )
    ]

    ax.legend(
        wedges,
        legend_labels,
        title="Keterangan",
        loc="lower center",
        bbox_to_anchor=(0.5, -0.1),
        frameon=False,
        borderaxespad=0.8
    )

    # Teks tengah donut
    ax.text(0, 0.06, "TOTAL", ha="center", va="center", fontsize=9, color="#666666")
    ax.text(0, -0.05, _fmt_thousands(total_all_status), ha="center", va="center",
            fontsize=14, fontweight="bold")

    ax.set_title("Proporsi Kelahiran berdasarkan Status Kelahiran")
    ax.set_aspect('equal')

    plt.show()
    print("- Visualisasi Status Kelahiran (Donut) Berhasil Ditampilkan ✓")

    print()
    print("-----------------------------------------------")
    print("Analisis dan Visualisasi Selesai ✓")
    print("-----------------------------------------------")

except Exception as e:
    print(f"- Gagal Membaca file : {path} : {e}")
