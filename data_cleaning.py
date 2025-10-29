# Import Lib
import pandas as pd
import os

# path rawdata
path = "./rawdata/rawdata_kelahiran_jawabarat_2012-2023.csv"

# Pastikan file ada
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
        
    # Baca File Excel
    df = pd.read_csv(path)
    print(f"- Berhasil Membaca File : {path} ✓")

    print()
    print("----------------------")
    print("Proses Cleaning Data ")
    print("----------------------")

    # Normalisasi Kolom
    df = df[['kode_kabupaten_kota', 'nama_kabupaten_kota', 
            'status_kelahiran', 'jenis_kelamin', 
            'jumlah_kelahiran', 'tahun']]
    print("- Normalisasi Kolom ✓")

    # Merapihkan Nama Kolom
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    print("- Merapihkan Nama Kolom ✓")

    # Ubah Tipe Data Kolom
    df['tahun'] = df['tahun'].astype(int)
    df['jumlah_kelahiran'] = df['jumlah_kelahiran'].astype(int)
    df['kode_kabupaten_kota'] = df['kode_kabupaten_kota'].astype(str)
    print("- Ubah Tipe Data Kolom ✓")

    # Hapus Duplicat Data
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"- Hapus Duplicat Data ({before - after} Baris) ✓")

    # Cek Nilai Kosong Perkolom
    print("- Cek Nilai Yang Kosong Perkolom ✓")
    print(df.isnull().sum())

    # Ubah Nilai Kosong Perkolom
    df['nama_kabupaten_kota'] = df['nama_kabupaten_kota'].fillna("Tidak Diketahui")
    df['jumlah_kelahiran'] = df['jumlah_kelahiran'].fillna(0)
    df['tahun'] = df['tahun'].fillna(0)
    print("- Ubah Nilai Yang Kosong Perkolom ✓")

    # Standarisasi Nilai
    df['nama_kabupaten_kota'] = df['nama_kabupaten_kota'].str.title().str.strip()
    df['jenis_kelamin'] = df['jenis_kelamin'].str.title().str.strip()
    df['status_kelahiran'] = df['status_kelahiran'].str.title().str.strip()
    print("- Standarisasi Nilai ✓")

    # Buat Folder final_dataset
    output_folder = "./final_dataset"
    os.makedirs(output_folder, exist_ok=True)

    # Tentukan nama file folder
    output_path = os.path.join(output_folder, "dataset_kelahiran_jawabarat_2012-2023.csv")
    
    # Simpan ke CSV di folder
    df.to_csv(output_path, index=False)
    print()
    print("--------")
    print("Selesai")
    print("--------")
    print(f"File CSV berhasil dibuat di: {output_path}")

except Exception as e:
    print(f"- Gagal Membaca file : {path} : {e}")

