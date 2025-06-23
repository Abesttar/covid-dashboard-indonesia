import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df = df[df["location"] == "Indonesia"]
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# Sidebar: Input tanggal
st.sidebar.title("📅 Filter Tanggal")
start_date = st.sidebar.date_input("Tanggal Mulai", df["date"].min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", df["date"].max().date())

if start_date > end_date:
    st.sidebar.error("Tanggal mulai tidak boleh setelah tanggal akhir.")

# Filter data
mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
filtered = df.loc[mask]

# Judul
st.title("📊 Dashboard COVID-19 Indonesia")
st.caption("Pantau jumlah kematian harian secara interaktif berdasarkan rentang tanggal pilihanmu.")

# Ringkasan data
col1, col2 = st.columns(2)
col1.metric("🗓️ Periode", f"{start_date} s.d. {end_date}")
col2.metric("💀 Total Kematian", int(filtered["new_deaths"].sum()))

# Grafik Interaktif
if not filtered.empty:
    st.subheader("📈 Grafik Kematian Harian (Interaktif)")
    fig = px.line(
        filtered,
        x="date",
        y="new_deaths",
        title="Kematian Harian COVID-19 di Indonesia",
        labels={"date": "Tanggal", "new_deaths": "Jumlah Kematian"},
        markers=True,
        template="plotly_dark",
    )
    fig.update_traces(line_color='red', marker=dict(size=6, color='white'))
    fig.update_layout(
        title_font_size=18,
        xaxis_title="Tanggal",
        yaxis_title="Jumlah Kematian",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Tidak ada data untuk tanggal yang dipilih.")
