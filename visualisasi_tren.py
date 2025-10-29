# ==================================================
# VISUALISASI TREN KELAHIRAN JAWA BARAT (2012–2023)
# ==================================================
# Import Lib
import pandas as pd
import matplotlib.pyplot as plt
import os

# path dataset
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

    # Baca dataset
    df = pd.read_csv(path)
    print(f"- Berhasil Membaca File : {path} ✓")

    # Filter tahun 2012–2023
    print()
    print("-----------------------------------------")
    print("Proses Analisis Deskriptif Tren Kelahiran")
    print("-----------------------------------------")
    df_filter = df[df['tahun'].between(2012, 2023)]
    print(f"- Filter Berdasarkan Tahun ✓")

    # Group Data Pertahun
    total_per_tahun = (
        df_filter.groupby('tahun')['jumlah_kelahiran']
        .sum()
        .reset_index()
        .sort_values('tahun')
    )

    # Menampilkan Data pertahun
    print(f"- Total Kelahiran Per Tahun ✓") 
    print()
    print("-------------------------------------------")
    print(f"{'Tahun':<10} {'Jumlah Kelahiran':>20}")
    print("-------------------------------------------")
    for index, row in total_per_tahun.iterrows():
        print(f"{int(row['tahun']):<10} {int(row['jumlah_kelahiran']):>20,}")

    # Data Tahun Tertinggi Dan Terendah
    tahun_max = total_per_tahun.loc[total_per_tahun['jumlah_kelahiran'].idxmax(), 'tahun']
    tahun_min = total_per_tahun.loc[total_per_tahun['jumlah_kelahiran'].idxmin(), 'tahun']
    max_value = total_per_tahun['jumlah_kelahiran'].max()
    min_value = total_per_tahun['jumlah_kelahiran'].min()
    print()
    print(f"- Tahun dengan Kelahiran Tertinggi : {tahun_max} ({max_value:,}) ✓")
    print(f"- Tahun dengan Kelahiran Terendah  : {tahun_min} ({min_value:,}) ✓")

    # Perubahan Data Tahun Ke Tahun
    print()
    print("- Perubahan Jumlah Tahun ke Tahun ✓")
    print("--------------------------------------------------------")
    print(f"{'Dari → Ke':<15} {'Arah':<10} {'Perubahan':>12} {'Persentase':>15}")
    print("--------------------------------------------------------")

    # Simpan hasil perubahan ke list
    perubahan_list = []
    persentase_list = []

    for i in range(1, len(total_per_tahun)):
        thn_lalu = total_per_tahun.loc[i-1, 'tahun']
        thn_skrg = total_per_tahun.loc[i, 'tahun']
        nilai_lalu = total_per_tahun.loc[i-1, 'jumlah_kelahiran']
        nilai_skrg = total_per_tahun.loc[i, 'jumlah_kelahiran']
        perubahan = nilai_skrg - nilai_lalu
        persentase = (perubahan / nilai_lalu) * 100

        arah = "Naik" if perubahan > 0 else "Turun"
        warna = "▲" if perubahan > 0 else "▼"

        print(f"{warna} {thn_lalu} → {thn_skrg:<8} {arah:<10} {abs(perubahan):>12,} {persentase:>13.2f}%")

        # Simpan data untuk visualisasi
        perubahan_list.append(perubahan)
        persentase_list.append(persentase)

    # --------------
    # VISUALISASI 
    # --------------

    print()
    print("-----------------------")
    print("Proses Visualisasi Data ")
    print("-----------------------")

    plt.figure(figsize=(11,6))
    print("- Membuat Canvas Grafik ✓")

    # Loop antar tahun untuk memberi warna per segmen
    print("- Membuat Line, Marker, dan Label di Atas Titik ✓")
    for i in range(len(total_per_tahun)):
        x = total_per_tahun['tahun'].iloc[i]
        y = total_per_tahun['jumlah_kelahiran'].iloc[i]

        # Warna berdasarkan perubahan dari tahun sebelumnya
        if i > 0:
            y_prev = total_per_tahun['jumlah_kelahiran'].iloc[i-1]
            color = 'green' if y > y_prev else 'red'
        else:
            color = 'gray' 
        
        # Plot titik dan garis 
        if i > 0:
            plt.plot(
                total_per_tahun['tahun'].iloc[i-1:i+1],
                total_per_tahun['jumlah_kelahiran'].iloc[i-1:i+1],
                color=color, linewidth=2.5, marker='o'
            )
        else:
            plt.plot(x, y, color=color, marker='o')

        # Hitung perubahan & persentase 
        if i > 0:
            perubahan = y - y_prev
            persentase = (perubahan / y_prev) * 100
            tanda = "▲" if perubahan > 0 else "▼"
            warna_teks = 'green' if perubahan > 0 else 'red'
            teks_persen = f"({persentase:+.2f}%)"
        else:
            tanda = ""
            warna_teks = 'gray'
            teks_persen = ""

        # Posisi label di atas marker
        offset = total_per_tahun['jumlah_kelahiran'].max() * 0.02
        plt.text(
            x,
            y + offset,
            f"{tanda} {int(y):,}\n{teks_persen}",
            color=warna_teks,
            fontsize=8,
            ha='center',
            va='bottom',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2)
        )

    # Atur sumbu Y 
    ymax = total_per_tahun['jumlah_kelahiran'].max()
    plt.ylim(0, (ymax // 100_000 + 1) * 100_000)

    # Format angka sumbu Y dengan ribuan
    plt.gca().get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{int(x):,}')
    )

    # Judul dan label
    plt.title("Tren Jumlah Kelahiran di Jawa Barat (2012–2023)", fontsize=14, fontweight='bold')
    plt.xlabel("Tahun", fontsize=12)
    plt.ylabel("Jumlah Kelahiran", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    print("- Menambahkan Judul, Label, dan Grid ✓")

    # Tambahkan legenda visual
    plt.text(2012.3, ymax*0.98, "▲ Naik", color='green', fontsize=10)
    plt.text(2012.3, ymax*0.95, "▼ Turun", color='red', fontsize=10)
    print("- Menambahkan Legenda ✓")

    plt.tight_layout()
    print("- Mengecek Element Grafik ✓")
    plt.show()
    print("- Visualisasi berhasil ditampilkan ✓")

    
except Exception as e:
    print(f"- Gagal Membaca file : {path} : {e}")
