import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data dari OWID
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

# Judul
st.title("📊 Dashboard COVID-19 Indonesia")
st.caption("Pantau jumlah kematian akibat COVID-19 berdasarkan bulan dan tahun.")

# Pilih bulan dan tahun
years = sorted(df["year"].unique())
months = list(range(1, 13))
month_names = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

col1, col2 = st.columns(2)
with col1:
    selected_year = st.selectbox("Pilih Tahun", years, index=len(years)-1)
with col2:
    selected_month = st.selectbox("Pilih Bulan", months, format_func=lambda x: month_names[x], index=6)

# Filter data
filtered = df[(df["year"] == selected_year) & (df["month"] == selected_month)]

# Jumlah kematian
total_deaths = filtered["new_deaths"].sum()
st.metric(label=f"Kematian pada {month_names[selected_month]} {selected_year}", value=int(total_deaths))

# Grafik
if not filtered.empty:
    st.subheader("📈 Grafik Kematian Harian")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.set_theme(style="whitegrid")
    sns.lineplot(data=filtered, x="date", y="new_deaths", marker="o", color="crimson", ax=ax)
    ax.set_title(f"Kematian Harian COVID-19 - {month_names[selected_month]} {selected_year}", fontsize=14)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Kematian")
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.warning("Data tidak tersedia untuk bulan/tahun yang dipilih.")
