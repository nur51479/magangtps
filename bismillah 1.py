import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Pemagang PT Terminal Petikemas Surabaya", layout="wide")

# Fungsi untuk memuat atau menyimpan data
@st.cache_data
def load_data():
    return pd.DataFrame(columns=["Nama", "Jurusan", "Institut", "Departemen", "Periode Mulai", "Periode Selesai", "Status"])

data = load_data()

# Sidebar untuk upload file
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload file Excel atau CSV", type=["xlsx", "csv"])
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)
    st.sidebar.success("File berhasil diunggah!")

# Halaman Input Data
st.title("Input Data Magang")

with st.form("input_data_form"):
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama")
        jurusan = st.text_input("Jurusan")
        institut = st.text_input("Institut")
    with col2:
        departemen = st.text_input("Departemen")
        periode_mulai = st.date_input("Periode Mulai", value=datetime.today())
        periode_selesai = st.date_input("Periode Selesai", value=datetime.today())
    status = st.selectbox("Status", ["Aktif", "Selesai", "Diperpanjang"])
    submit = st.form_submit_button("Add")

    if submit:
        new_data = pd.DataFrame({
            "Nama": [nama],
            "Jurusan": [jurusan],
            "Institut": [institut],
            "Departemen": [departemen],
            "Periode Mulai": [periode_mulai],
            "Periode Selesai": [periode_selesai],
            "Status": [status]
        })
        data = pd.concat([data, new_data], ignore_index=True)
        st.success("Data berhasil ditambahkan!")

# Halaman Data
st.title("Data Pemagang")
data = st.data_editor(data, num_rows="dynamic")

# Halaman Dashboard
st.title("Dashboard Magang PT TPS")
col1, col2 = st.columns(2)

with col1:
    status_filter = st.selectbox("Filter Status", ["Semua"] + list(data["Status"].unique()))
    periode_filter = st.slider("Pilih Periode Tahun", int(data["Periode Mulai"].dt.year.min()), int(data["Periode Selesai"].dt.year.max()), (2020, 2025))

data_filtered = data.copy()
if status_filter != "Semua":
    data_filtered = data_filtered[data_filtered["Status"] == status_filter]
data_filtered = data_filtered[(data_filtered["Periode Mulai"].dt.year >= periode_filter[0]) & (data_filtered["Periode Selesai"].dt.year <= periode_filter[1])]

with col2:
    total_pemagang = len(data_filtered)
    st.metric(label="Total Pemagang", value=total_pemagang)

# Bar chart jumlah magang per departemen
st.subheader("Jumlah Pemagang per Departemen")
departemen_count = data_filtered["Departemen"].value_counts().reset_index()
departemen_count.columns = ["Departemen", "Jumlah"]
fig = px.bar(departemen_count, x="Departemen", y="Jumlah", text="Jumlah", color="Departemen", height=500)
st.plotly_chart(fig)
