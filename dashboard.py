# ==============================================================
# DASHBOARD ANALISIS JUMLAH KELAHIRAN DI JAWA BARAT (2012–2025)
# ==============================================================
import streamlit as st
import os
import io
import runpy
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
from contextlib import redirect_stdout

# -------------------------------
# Konfigurasi halaman
# -------------------------------
st.set_page_config(
    page_title="Dashboard Analisis Jumlah Kelahiran di Jawa Barat (2012–2025)",
    layout="wide",
    page_icon="👶"
)

st.title("Dashboard Analisis Jumlah Kelahiran di Jawa Barat (2012–2025)")
st.caption("Disusun oleh **Yoga Saputra**, **Budi Agung**, **Syah Irul Mahruf**, **Valentino Febriankus** ")

# -------------------------------
# Fungsi bantu
# -------------------------------
def tampilkan_grafik(file_path):
    """Menjalankan file Python dan menampilkan grafik Matplotlib di Streamlit"""
    try:
        with io.StringIO() as buf, redirect_stdout(buf):
            plt.close('all')
            runpy.run_path(file_path)
            output = buf.getvalue()
        figs = [plt.figure(i) for i in plt.get_fignums()]
        if figs:
            for fig in figs:
                st.pyplot(fig)
        else:
            st.warning("⚠️ Tidak ada grafik yang dihasilkan dari file ini.")
    except Exception as e:
        st.error(f"❌ Terjadi error saat menampilkan grafik: {e}")

# -------------------------------
# Sidebar Navigasi
# -------------------------------
pages = [
    "Dashboard",
    "Tren Tahunan",
    "Distribusi Kabupaten/Kota",
    "Heatmap Persebaran",
    "Jenis Kelamin & Status",
    "Prediksi (2024–2025)",
    "Kesimpulan Dan Saran"
]

# Simpan index halaman di session_state agar tombol next/previous bisa berfungsi
if "page_index" not in st.session_state:
    st.session_state.page_index = 0

# Sidebar Radio
menu = st.sidebar.radio("Pilih Halaman:", pages, index=st.session_state.page_index)
base_path = os.path.dirname(os.path.abspath(__file__))

# -------------------------------
# Fungsi untuk update halaman
# -------------------------------
def go_next():
    if st.session_state.page_index < len(pages) - 1:
        st.session_state.page_index += 1
        st.rerun()

def go_prev():
    if st.session_state.page_index > 0:
        st.session_state.page_index -= 1
        st.rerun()

# -------------------------------
# Tampilan halaman
# -------------------------------
if menu == "Dashboard":
    st.subheader("Ringkasan Analisis")
    st.markdown("""
    - **Dataset:** Jumlah Kelahiran Bayi Berdasarkan Status Kelahiran dan Jenis Kelamin di Jawa Barat Tahun 2012–2023 
    - **Periode Data:** 2012–2023  
    - **Sumber:** [Open Data Jabar](https://opendata.jabarprov.go.id/id/dataset/jumlah-kelahiran-bayi-berdasarkan-status-kelahiran-dan-jenis-kelamin-di-jawa-barat)   
    - **Library Analisis Data:** Pandas, Numpy, Statsmodels ARIMA, Sklearn
    - **Library Visualisasi:** Matplotlib, Folium, Plotly, Streamlit
    """)

    st.markdown("""
   ### **Tujuan Analisis**
    Analisis ini bertujuan untuk:
    1. Menganalisis tren pertumbuhan jumlah kelahiran** di Provinsi Jawa Barat selama periode 2012–2023.  
    2. Membandingkan angka kelahiran hidup dan kelahiran mati sebagai gambaran kondisi demografi masyarakat Jawa Barat.  
    3. Mengidentifikasi distribusi kelahiran berdasarkan jenis kelamin dan wilayah kabupaten/kota guna mengetahui daerah dengan angka kelahiran tertinggi dan terendah.  
    4. Menyajikan hasil analisis dalam bentuk visualisasi interaktif dan informatif menggunakan bahasa pemrograman Python dengan library seperti Matplotlib, Folium, Plotly, Streamlit.  
    5. Mengevaluasi keterkaitan antara program Keluarga Berencana (KB) serta sosialisasi vasektomi dengan tren penurunan angka kelahiran di Jawa Barat.  
    6. Memprediksi pertumbuhan jumlah kelahiran 1–2 tahun ke depan** menggunakan model time series sebagai bahan pertimbangan dalam perencanaan kebijakan kependudukan.
    """)

    st.markdown("""
    ### **Metodologi**
    1. Data Collection: Mengambil dataset resmi dari portal Open Data Jabar.  
    2. Data Cleaning & Transformation: Menghapus duplikasi, memperbaiki format kolom, dan menggabungkan data lintas tahun.  
    3. Descriptive Analysis: Menggunakan agregasi dan statistik deskriptif untuk menghitung tren dan total kelahiran.  
    4. Data Visualization:
       - *Line Chart* untuk tren tahunan  
       - *Bar Chart* untuk distribusi kabupaten/kota  
       - *Heatmap Folium* untuk peta geografis  
       - *Donut Chart* untuk jenis kelamin dan status  
    5. Predictive Modelling: Model Time Series ARIMA digunakan untuk memprediksi dua tahun ke depan (2024–2025).  
    """)

# -------------------------------
elif menu == "Tren Tahunan":
    st.subheader("Tren Jumlah Kelahiran per Tahun (2012–2023)")
    file_path = os.path.join(base_path, "visualisasi_tren.py")
    tampilkan_grafik(file_path)

    st.markdown("""
    ### Insight:
    - Fluktuasi yang Terlihat:
      Grafik menunjukkan pola naik-turun yang cukup tajam, terutama pada tahun 2014–2015, yang kemungkinan dipengaruhi oleh kebijakan kesehatan, kondisi ekonomi, dan faktor sosial masyarakat.
    - Puncak Kelahiran Tahun 2017:
      Peningkatan pada tahun 2016–2017 menunjukkan adanya faktor pendukung seperti perbaikan pelayanan kesehatan dan akses persalinan.
    - Penurunan Saat Pandemi (2019–2020):
      Penurunan pada periode ini bisa dikaitkan dengan pandemi COVID-19, dimana terjadi pembatasan aktivitas dan penurunan pelayanan kesehatan reproduksi.
    - Pemulihan Pasca Pandemi:
      Tahun 2021 menunjukkan pemulihan dengan kenaikan sebesar +9,87%, walaupun tren kembali melandai pada tahun berikutnya
    """)

# -------------------------------
elif menu == "Distribusi Kabupaten/Kota":
    st.subheader("Distribusi Jumlah Kelahiran per Kabupaten/Kota (2012–2023)")
    file_path = os.path.join(base_path, "visualisasi_kabupaten_kota.py")
    tampilkan_grafik(file_path)

    st.markdown("""
    ### Insight:
    - Konsentrasi di Wilayah Padat Penduduk:
      Grafik menunjukkan dominasi kabupaten besar seperti Bogor, Bekasi, dan Bandung. Hal ini menggambarkan korelasi antara kepadatan penduduk dan jumlah kelahiran.
    - Perbedaan Peran Kota dan Kabupaten:
      Kota cenderung memiliki angka kelahiran lebih rendah karena pergeseran gaya hidup, tingkat pendidikan, dan kesadaran terhadap program KB yang lebih tinggi.
    - Tantangan Pemerintah Daerah:
      Pemerintah perlu memberikan perhatian lebih pada wilayah dengan kelahiran tinggi untuk memperkuat sosialisasi program KB dan vasektomi, serta memperluas akses terhadap pelayanan kesehatan reproduksi.
    - Efektivitas Program KB di Daerah:
      Wilayah dengan angka kelahiran rendah bisa menjadi contoh keberhasilan program KB dan edukasi keluarga berencana yang efektif
    """)

# -------------------------------
elif menu == "Heatmap Persebaran":
    st.subheader("Peta Persebaran Kelahiran di Jawa Barat (2012–2023)")
    file_path = os.path.join(base_path, "visualisasi_heatmap_kelahiran.py")
    tampilkan_grafik(file_path)

    map_path = os.path.join(base_path, "visualisasi", "heatmap_kelahiran_jawabarat_2012-2023.html")
    if os.path.exists(map_path):
        with open(map_path, "r", encoding="utf-8") as f:
            html_data = f.read()
        components.html(html_data, height=700)
    else:
        st.warning("⚠️ File peta heatmap belum ditemukan. Jalankan ulang script heatmap terlebih dahulu.")

    st.markdown("""
    ### Insight:
    - Kabupaten Bogor, Kota Bekasi dan Kota Bandung merupakan wilayah dengan tingkat kelahiran tertinggi selama periode 2012–2023. Wilayah-wilayah ini ditunjukkan dengan warna merah pekat pada peta. Hal ini dapat dikaitkan dengan jumlah penduduk yang besar, tingkat urbanisasi tinggi, dan akses layanan kesehatan yang memadai.
    - Kabupaten Garut, Kabupaten Tasikmalaya, dan Kabupaten Subang menunjukkan tingkat kelahiran menengah yang ditandai dengan gradasi warna hijau hingga kuning. Wilayah ini memiliki kepadatan penduduk cukup tinggi namun tidak sepadat kawasan metropolitan.
    - Kabupaten Pangandaran, Kota Banjar, dan Kabupaten Kuningan menampilkan intensitas kelahiran yang rendah, ditunjukkan dengan warna biru muda. Faktor penyebabnya antara lain kepadatan penduduk yang rendah, wilayah pedesaan yang luas, serta tingkat pertumbuhan penduduk yang lebih stabil.
    - Pola konsentrasi kelahiran di wilayah metropolitan yang menjadi pusat aktivitas ekonomi dan sosial, seperti Kota Bandung dan Kota Bekasi.
    - Wilayah dengan akses kesehatan dan kepadatan penduduk rendah, seperti Kabupaten Pangandaran dan Kota Banjar, menunjukkan aktivitas kelahiran yang lebih jarang.
    - Perbedaan warna pada peta membantu dalam mengidentifikasi prioritas wilayah untuk program pemerintah di bidang kesehatan ibu dan anak, perencanaan keluarga, serta pembangunan fasilitas publik.

    """)

# -------------------------------
elif menu == "Jenis Kelamin & Status":
    st.subheader("Proporsi Berdasarkan Jenis Kelamin & Status Kelahiran (2012–2023)")
    file_path = os.path.join(base_path, "visualisasi_jenis_status.py")
    tampilkan_grafik(file_path)

    st.markdown("""
    ### Insight:
    - Laki-laki: sekitar 50,6% dari total kelahiran.  
    - Perempuan: sekitar 49,4% dari total kelahiran.
    - Proporsi kelahiran laki-laki sedikit lebih tinggi dibanding perempuan, namun selisihnya tidak signifikan.  
    - Kondisi ini menunjukkan keseimbangan alami antara jumlah kelahiran kedua jenis kelamin di Jawa Barat.
    - Kelahiran hidup: mencapai 99,74%, sedangkan kelahiran mati hanya 0,26%.  
    - Menunjukkan pelayanan kesehatan ibu & anak di Jawa Barat cukup baik.
    - Pemerintah dapat memanfaatkan informasi ini untuk perencanaan kebijakan kesehatan anak dan pendidikan yang lebih proporsional antara gender laki-laki dan perempuan



    """)

# -------------------------------
elif menu == "Prediksi (2024–2025)":
    st.subheader("Prediksi Jumlah Kelahiran di Jawa Barat (2024–2025)")
    file_path = os.path.join(base_path, "visualisasi_prediksi_kelahiran.py")
    tampilkan_grafik(file_path)

    st.markdown("""
    ### Insight:
    - Model Time Series ARIMA memperkirakan penurunan tipis pada dua tahun mendatang.  
    - Prediksi 2024: sekitar 860.500 kelahiran.  
    - Prediksi 2025: sekitar 842.300 kelahiran.  
    - Mengindikasikan stabilisasi populasi dan meningkatnya kesadaran keluarga berencana.  
    
    """)

# -------------------------------
elif menu == "Kesimpulan Dan Saran":
    st.subheader("Kesimpulan Dan Saran")
    st.markdown("""
    ### KESIMPULAN:
    Berdasarkan hasil analisis dan visualisasi data jumlah kelahiran di Provinsi Jawa Barat selama periode 2012–2023, dapat diambil beberapa kesimpulan sebagai berikut:

    - Tren Kelahiran Fluktuatif tetapi Cenderung Stabil.
      Data menunjukkan bahwa jumlah kelahiran di Jawa Barat mengalami fluktuasi dari tahun ke tahun. Puncak tertinggi terjadi pada tahun 2017 dengan 917.556 kelahiran, sedangkan jumlah terendah terjadi pada tahun 2014 dengan 333.441 kelahiran. Setelah 2018, tren kelahiran cenderung stabil di kisaran 800–850 ribu per tahun.
    - Dampak Pandemi terhadap Angka Kelahiran.
      Penurunan signifikan terlihat pada periode 2019–2020, yang kemungkinan besar disebabkan oleh dampak pandemi COVID-19 yang membatasi akses pelayanan kesehatan serta aktivitas masyarakat. Namun, pada tahun 2021, tren kembali meningkat menandakan adanya pemulihan pasca pandemi.
    - Distribusi Wilayah yang Tidak Merata.
      Kabupaten Bogor menjadi wilayah dengan jumlah kelahiran tertinggi selama periode pengamatan, mencapai lebih dari 1,4 juta kelahiran, diikuti oleh Kabupaten Bekasi, Bandung, dan Kota Depok. Sementara itu, Kota Banjar dan Kabupaten Pangandaran memiliki jumlah kelahiran terendah.Pola ini menunjukkan bahwa daerah dengan kepadatan penduduk tinggi cenderung memiliki tingkat kelahiran lebih besar.
    - Proporsi Jenis Kelamin Seimbang.
      Dari hasil visualisasi pie chart, diperoleh total 50,45% kelahiran laki-laki dan 49,55% kelahiran perempuan. Perbandingan ini menunjukkan rasio jenis kelamin yang relatif seimbang, sesuai dengan pola demografi nasional.
    - Kualitas Kesehatan Ibu dan Anak Meningkat.
      Berdasarkan data, 99,73% kelahiran tercatat hidup, sedangkan 0,27% merupakan kelahiran mati. Hal ini menunjukkan bahwa tingkat keberhasilan persalinan di Jawa Barat tergolong sangat baik dan menunjukkan peningkatan kualitas pelayanan kesehatan ibu dan anak.
    - Prediksi Kelahiran 2024–2025 Menunjukkan Penurunan Ringan.
      Model prediksi menggunakan TIME SERIES ARIMA memperkirakan jumlah kelahiran sebesar 850.180 jiwa pada tahun 2024 dan menurun sedikit menjadi 824.796 jiwa pada tahun 2025. Hal ini menunjukkan kecenderungan stabil dengan potensi penurunan kecil dalam dua tahun ke depan.
    - Pemanfaatan Python Efektif untuk Analisis dan Visualisasi.
      Bahasa pemrograman Python beserta pustaka seperti Matplotlib, Seaborn, dan Plotly terbukti efektif dalam mengolah, menganalisis, dan menampilkan data secara informatif dan interaktif. Visualisasi yang dihasilkan membantu memahami pola kelahiran secara lebih mendalam dan komunikatif.

    """)

    st.markdown("""
    ### SARAN:
    Berdasarkan hasil analisis dan kesimpulan di atas, beberapa saran yang dapat diajukan adalah sebagai berikut:

    - Untuk Pemerintah Daerah dan Instansi Terkait
      Perlu memperkuat program Keluarga Berencana (KB) terutama di wilayah dengan tingkat kelahiran tinggi seperti Kabupaten Bogor, Bekasi, dan Bandung.
      Meningkatkan edukasi kesehatan reproduksi bagi masyarakat, khususnya pasangan usia subur, agar kesadaran tentang perencanaan keluarga semakin meningkat.
      Memperluas akses layanan kesehatan ibu dan anak di wilayah pedesaan atau kabupaten dengan angka kelahiran mati yang masih ada.

    - Untuk Lembaga Pendidikan dan Akademisi
      Analisis ini dapat dijadikan studi kasus nyata dalam pembelajaran tentang grafik dan visualisasi data, khususnya dalam penerapan bahasa pemrograman Python.
      Perlu dilakukan penelitian lanjutan dengan menambahkan variabel lain seperti pendapatan per kapita, tingkat pendidikan, dan fasilitas kesehatan, agar hasil analisis lebih komprehensif.
    
    - Untuk Masyarakat Umum:
      Diharapkan semakin meningkatkan kesadaran pentingnya perencanaan keluarga dan kesehatan ibu hamil.
      Masyarakat dapat memanfaatkan informasi hasil visualisasi data ini sebagai dasar dalam memahami kondisi kependudukan di daerah masing-masing.
    
    - Untuk Pengembangan Analisis Selanjutnya:
      Dapat dikembangkan dashboard interaktif berbasis web menggunakan Plotly atau Dash agar data kelahiran dapat diakses secara real-time oleh publik dan instansi pemerintah.
      Penggunaan model prediktif lanjutan seperti machine learning (misalnya LSTM atau Prophet) dapat meningkatkan akurasi prediksi kelahiran di masa depan.

    """)

# -------------------------------
# Tombol Navigasi (Next / Previous)
# -------------------------------
st.markdown("---")
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.session_state.page_index > 0:
        if st.button("< Previous"):
            go_prev()
with col3:
    if st.session_state.page_index < len(pages) - 1:
        if st.button("Next >"):
            go_next()

# -------------------------------
# Footer
# -------------------------------
st.caption("© 2025 | Analisis Data Kelahiran Jawa Barat — Universitas Dian Nusantara")
