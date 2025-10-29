# ==============================================================
# PREDIKSI TREN JUMLAH KELAHIRAN DI JAWA BARAT (2024–2025)
# MENGGUNAKAN MODEL TIME SERIES ARIMA
# ==============================================================

# Import Library
import pandas as pd
import matplotlib.pyplot as plt
import os
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

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

# Membaca File
print()
print("----------------------")
print("Proses Membaca File ")
print("----------------------")

try:
    df = pd.read_csv(path)
    print(f"- Berhasil Membaca File : {path} ✓")

    # Filter tahun 2012–2023
    print()
    print("--------------------------------------------")
    print("Proses Analisis Deret Waktu (Time Series) ")
    print("--------------------------------------------")
    df_filter = df[df['tahun'].between(2012, 2023)]
    print(f"- Filter Berdasarkan Tahun ✓")

    # Agregasi total per tahun
    df_tahunan = (
        df_filter.groupby('tahun')['jumlah_kelahiran']
        .sum()
        .reset_index()
        .sort_values('tahun')
    )
    print("- Menghitung Total Kelahiran per Tahun ✓")

    # Set kolom tahun sebagai index (untuk ARIMA)
    df_tahunan.set_index('tahun', inplace=True)
    series = df_tahunan['jumlah_kelahiran']

    print()
    print("-------------------------------")
    print("Proses Pembuatan Model ARIMA")
    print("-------------------------------")

    # Inisialisasi model ARIMA
    model = ARIMA(series, order=(1,1,1))  # p,d,q = 1,1,1 (model umum untuk tren)
    model_fit = model.fit()
    print("- Model ARIMA(1,1,1) Berhasil Dibentuk ✓")

    # Lakukan prediksi ke depan (2 tahun: 2024–2025)
    forecast = model_fit.forecast(steps=2)
    tahun_prediksi = [2024, 2025]
    hasil_prediksi = pd.DataFrame({
        'Tahun': tahun_prediksi,
        'Prediksi_Kelahiran': forecast.astype(int)
    })

    print()
    print("----------------------------")
    print("Hasil Prediksi Kelahiran")
    print("----------------------------")
    for _, row in hasil_prediksi.iterrows():
        print(f"- Tahun {int(row['Tahun'])} : {int(row['Prediksi_Kelahiran']):,} kelahiran")

    # Gabungkan data aktual + prediksi untuk visualisasi
    df_visual = df_tahunan.copy()
    for i in range(len(hasil_prediksi)):
        df_visual.loc[hasil_prediksi['Tahun'].iloc[i]] = hasil_prediksi['Prediksi_Kelahiran'].iloc[i]

    # -----------------------------------
    # VISUALISASI HASIL PREDIKSI ARIMA
    # -----------------------------------
    print()
    print("----------------------------")
    print("Proses Visualisasi Prediksi ")
    print("----------------------------")

    plt.figure(figsize=(10,6))
    print("- Membuat Canvas Grafik ✓")

    # Plot data aktual
    plt.plot(df_tahunan.index, df_tahunan['jumlah_kelahiran'], marker='o', color='blue', label='Data Aktual (2012–2023)')
    
    # Plot data prediksi
    plt.plot(hasil_prediksi['Tahun'], hasil_prediksi['Prediksi_Kelahiran'], marker='o', color='orange', linestyle='--', label='Prediksi (2024–2025)')

    # Tambahkan titik dan label prediksi
    for _, row in hasil_prediksi.iterrows():
        plt.text(
            row['Tahun'], row['Prediksi_Kelahiran'] + 10000,
            f"{int(row['Prediksi_Kelahiran']):,}",
            ha='center', color='orange', fontsize=9, fontweight='bold'
        )

    # Pengaturan grafik
    plt.title("Prediksi Jumlah Kelahiran \n Jawa Barat 2024–2025 \n (Model Time Series ARIMA)", fontsize=13, fontweight='bold')
    plt.xlabel("Tahun", fontsize=11)
    plt.ylabel("Jumlah Kelahiran", fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()

    print("- Menambahkan Judul, Label, dan Legenda ✓")

    # Simpan hasil visualisasi
    output_path = "./visualisasi/prediksi_kelahiran_arima_2024-2025.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.show()
    print(f"- Visualisasi Berhasil Disimpan di: {output_path} ✓")

    print()
    print("---------------------------------------------")
    print("Analisis & Visualisasi Prediksi Selesai ✓")
    print("---------------------------------------------")

except Exception as e:
    print(f"- Gagal Membaca file : {path} : {e}")
