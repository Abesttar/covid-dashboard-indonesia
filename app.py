import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df = df[df["location"] == "Indonesia"]
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# Sidebar - input tanggal
st.sidebar.title("📅 Filter Tanggal")
start_date = st.sidebar.date_input("Tanggal Mulai", df["date"].min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", df["date"].max().date())

if start_date > end_date:
    st.sidebar.error("Tanggal mulai tidak boleh setelah tanggal akhir.")

# Filter data
mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
filtered = df.loc[mask]

# Judul dan ringkasan
st.title("📊 Dashboard COVID-19 Indonesia")
st.markdown("Pantau jumlah kematian harian akibat COVID-19 berdasarkan rentang tanggal yang dipilih.")

col1, col2 = st.columns(2)
col1.metric("📆 Periode", f"{start_date} s.d. {end_date}")
col2.metric("💀 Total Kematian", int(filtered["new_deaths"].sum()))

# Grafik
if not filtered.empty:
    st.subheader("📈 Grafik Kematian Harian")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.set_theme(style="darkgrid")
    sns.lineplot(data=filtered, x="date", y="new_deaths", marker="o", color="#e63946", ax=ax)
    ax.set_title("Jumlah Kematian Harian COVID-19", fontsize=16)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Kematian")
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.warning("Tidak ada data untuk tanggal yang dipilih.")
