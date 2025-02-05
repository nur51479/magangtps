import streamlit as st
import pandas as pd
from io import BytesIO

# Inisialisasi session state untuk menyimpan data jika belum ada
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Nama", "Departemen", "Instansi", "Jurusan", "Jalur Magang", "Periode Magang", "Status Magang"
    ])

st.title("Dashboard Input Data Magang")

# --- UPLOAD FILE EXCEL ---
st.subheader("Upload File Excel")
uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx", "xls"])

if uploaded_file:
    df_uploaded = pd.read_excel(uploaded_file)
    st.session_state.data = pd.concat([st.session_state.data, df_uploaded], ignore_index=True)
    st.success("Data dari file Excel berhasil ditambahkan!")

# --- INPUT DATA MANUAL ---
st.subheader("Tambah Data Manual")

with st.form("form_tambah_data"):
    nama = st.text_input("Nama")
    departemen = st.text_input("Departemen")
    instansi = st.text_input("Instansi")
    jurusan = st.text_input("Jurusan")
    jalur_magang = st.selectbox("Jalur Magang", ["Reguler", "Kampus Merdeka", "Mandiri"])
    periode_magang = st.text_input("Periode Magang")
    status_magang = st.selectbox("Status Magang", ["Aktif", "Selesai", "Dibatalkan"])
    tambah_data = st.form_submit_button("Add Data")
    
    if tambah_data:
        new_data = pd.DataFrame({
            "Nama": [nama],
            "Departemen": [departemen],
            "Instansi": [instansi],
            "Jurusan": [jurusan],
            "Jalur Magang": [jalur_magang],
            "Periode Magang": [periode_magang],
            "Status Magang": [status_magang]
        })
        st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
        st.success("Data berhasil ditambahkan!")

# --- TAMPILKAN DATA ---
st.subheader("Tabel Data Magang")
st.dataframe(st.session_state.data)

# --- DOWNLOAD DATA ---
st.subheader("Download Data")
output = BytesIO()
st.session_state.data.to_excel(output, index=False, engine='xlsxwriter')
output.seek(0)
st.download_button(
    label="Download Excel",
    data=output,
    file_name="data_magang.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
