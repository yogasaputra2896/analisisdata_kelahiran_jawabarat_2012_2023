# ==============================================================
# VISUALISASI HEATMAP GEOGRAFIS KELAHIRAN JAWA BARAT (2012–2023)
# DENGAN GARIS BATAS WILAYAH (GEOJSON) & TOOLTIP INTERAKTIF
# ==============================================================
# Import Library
import pandas as pd
import folium
from folium.plugins import HeatMap
import os
import numpy as np
import requests

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

    # Koordinat pusat setiap Kabupaten/Kota di Jawa Barat
    lokasi = {
        'Kabupaten Bogor': (-6.479679, 106.824965),
        'Kabupaten Sukabumi': (-6.915727, 106.932576),
        'Kabupaten Cianjur': (-6.822558, 107.139542),
        'Kabupaten Bandung': (-7.012851, 107.528627),
        'Kabupaten Garut': (-7.202988, 107.885592),
        'Kabupaten Tasikmalaya': (-7.361212, 108.112488),
        'Kabupaten Ciamis': (-7.325788, 108.3514),
        'Kabupaten Kuningan': (-6.976233, 108.482982),
        'Kabupaten Cirebon': (-6.764507, 108.478858),
        'Kabupaten Majalengka': (-6.8361, 108.2270),
        'Kabupaten Sumedang': (-6.8607, 107.9201),
        'Kabupaten Indramayu': (-6.337707, 108.320823),
        'Kabupaten Subang': (-6.571549, 107.762495),
        'Kabupaten Purwakarta': (-6.551701, 107.446541),
        'Kabupaten Karawang': (-6.301721, 107.30529),
        'Kabupaten Bekasi': (-6.364614, 107.172509),
        'Kabupaten Bandung Barat': (-6.840651, 107.512302),
        'Kabupaten Pangandaran': (-7.701397, 108.495155),
        'Kota Bogor': (-6.594946, 106.794913),
        'Kota Sukabumi': (-6.918366, 106.931496),
        'Kota Bandung': (-6.910786, 107.609757),
        'Kota Cirebon': (-6.707076, 108.557818),
        'Kota Bekasi': (-6.236221, 106.994293),
        'Kota Depok': (-6.394473, 106.822692),
        'Kota Cimahi': (-6.87121, 107.555486),
        'Kota Tasikmalaya': (-7.316436, 108.1971),
        'Kota Banjar': (-7.362487, 108.55887),
    }

    # Tambahkan kolom latitude & longitude berdasarkan nama wilayah
    df['latitude'] = df['nama_kabupaten_kota'].map(lambda x: lokasi.get(x, (-6.9, 107.6))[0])
    df['longitude'] = df['nama_kabupaten_kota'].map(lambda x: lokasi.get(x, (-6.9, 107.6))[1])

    # Cek wilayah yang berhasil dipetakan
    mapped = df['nama_kabupaten_kota'].isin(lokasi.keys()).sum()
    print(f"- Wilayah Berhasil Dipetakan: {mapped} dari {df['nama_kabupaten_kota'].nunique()} ✓")

    # Filter tahun 2012–2023
    print()
    print("----------------------------------------------")
    print("Proses Analisis Persebaran Geografis Kelahiran")
    print("----------------------------------------------")
    df_filter = df[df['tahun'].between(2012, 2023)]
    print(f"- Filter Berdasarkan Tahun ✓")

    # Kelompokkan data berdasarkan wilayah
    df_geo = (
        df_filter.groupby(['nama_kabupaten_kota', 'latitude', 'longitude'])['jumlah_kelahiran']
        .sum()
        .reset_index()
        .sort_values('jumlah_kelahiran', ascending=False)
    )
    print(f"- Mengelompokkan Data Kelahiran per Wilayah dengan Koordinat ✓")

    # -------------------------------------------------------------
    # Tampilkan seluruh hasil (27 kabupaten/kota)
    # -------------------------------------------------------------
    print()
    print("--------------------------------------------------------------------------")
    print(f"{'Kabupaten/Kota':<30} {'Latitude':>10} {'Longitude':>12} {'Total Kelahiran':>20}")
    print("--------------------------------------------------------------------------")

    for _, row in df_geo.iterrows():
        print(f"{row['nama_kabupaten_kota']:<30} {row['latitude']:>10.4f} {row['longitude']:>12.4f} {int(row['jumlah_kelahiran']):>20,}")

    print("--------------------------------------------------------------------------")

    # Cari wilayah tertinggi dan terendah
    kota_max = df_geo.loc[df_geo['jumlah_kelahiran'].idxmax(), 'nama_kabupaten_kota']
    kota_min = df_geo.loc[df_geo['jumlah_kelahiran'].idxmin(), 'nama_kabupaten_kota']
    max_val = df_geo['jumlah_kelahiran'].max()
    min_val = df_geo['jumlah_kelahiran'].min()

    print(f"- Wilayah dengan Kelahiran Tertinggi : {kota_max} ({max_val:,}) ✓")
    print(f"- Wilayah dengan Kelahiran Terendah  : {kota_min} ({min_val:,}) ✓")
    print(f"- Total Wilayah Tercakup: {len(df_geo)} Kabupaten/Kota ✓")

    # -----------------------
    # VISUALISASI HEATMAP
    # -----------------------
    print()
    print("------------------------------------")
    print("Proses Visualisasi Heatmap Geografis ")
    print("------------------------------------")

    # Buat peta dasar
    m = folium.Map(location=[-6.9, 107.6], zoom_start=8, tiles="cartodbpositron")
    print("- Membuat Canvas Peta Jawa Barat ✓")

    # Gunakan intensitas dinamis berdasarkan jumlah kelahiran
    heat_data = [
        [row['latitude'], row['longitude'], row['jumlah_kelahiran'] / 10000]
        for _, row in df_geo.iterrows()
    ]
    HeatMap(heat_data, radius=40, blur=25, max_zoom=10, min_opacity=0.4).add_to(m)
    print("- Menambahkan Layer HeatMap ke Peta ✓")

    # Tambahkan marker tooltip interaktif
    for _, row in df_geo.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=4,
            color='green',
            fill=True,
            fill_opacity=0.7,
            tooltip=f"<b>{row['nama_kabupaten_kota']}</b><br>Total Kelahiran: {int(row['jumlah_kelahiran']):,}"
        ).add_to(m)
    print("- Menambahkan Tooltip Kabupaten/Kota ✓")

    # -------------------------------
    # Tambahkan Garis Batas Wilayah
    # -------------------------------
    print()
    print("----------------------------")
    print("Menambahkan Garis Batas Wilayah Jawa Barat")
    print("----------------------------")

    geojson_url = "https://github.com/hitamcoklat/Jawa-Barat-Geo-JSON/blob/master/Jabar_By_Kab.geojson?raw=true"

    try:
        r = requests.get(geojson_url)
        if r.status_code == 200:
            data_geojson = r.json()
            folium.GeoJson(
                data_geojson,
                name="Batas Wilayah Jawa Barat",
                style_function=lambda x: {
                    'fillColor': 'none',
                    'color': 'green',
                    'weight': 3,
                    'opacity': 0.6
                }
            ).add_to(m)
            print("- Garis Batas Wilayah Jawa Barat Berhasil Ditambahkan ✓")
        else:
            print(f"- Gagal Mengunduh GeoJSON (Status {r.status_code})")

    except Exception as e:
        print(f"- Gagal Menambahkan Garis Batas Wilayah: {e}")

    # Tambahkan judul peta
    title_html = '''
        <h3 align="center" style="font-size:16px"><b>Peta Heatmap Intensitas Kelahiran di Jawa Barat (2012–2023)</b></h3>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    print("- Menambahkan Judul Peta ✓")

    # Simpan hasil peta
    output_path = "./visualisasi/heatmap_kelahiran_jawabarat_2012-2023.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    m.save(output_path)
    print(f"- Peta Heatmap Berhasil Disimpan di: {output_path} ✓")

    print()
    print("--------------------------------------------")
    print("Analisis dan Visualisasi Heatmap Geografis Selesai ✓")
    print("--------------------------------------------")

except Exception as e:
    print(f"- Gagal Membaca file : {path} : {e}")
