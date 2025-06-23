
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df = df[df["location"] == "Indonesia"]
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    return df

# Load data
df = load_data()

# Judul dashboard
st.title("📊 Dashboard COVID-19 Indonesia")
st.write("Pantau jumlah kematian akibat COVID-19 berdasarkan bulan dan tahun.")

# Buat daftar tahun & bulan unik
years = sorted(df["year"].unique())
months = list(range(1, 13))
month_names = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

# Pilihan input pengguna
col1, col2 = st.columns(2)
with col1:
    selected_year = st.selectbox("Pilih Tahun", years, index=len(years)-1)
with col2:
    selected_month = st.selectbox("Pilih Bulan", months, format_func=lambda x: month_names[x], index=6)

# Filter data sesuai input
filtered = df[(df["year"] == selected_year) & (df["month"] == selected_month)]

# Tampilkan total kematian dalam bulan terpilih
total_deaths = filtered["new_deaths"].sum()
st.metric(label=f"Kematian COVID-19 pada {month_names[selected_month]} {selected_year}", value=int(total_deaths))

# (Opsional) Tampilkan grafik harian kematian
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(filtered["date"], filtered["new_deaths"], marker="o", linestyle="-", color="red")
ax.set_title("Tren Kematian Harian")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Kematian")
ax.grid(True)
st.pyplot(fig)
