import streamlit as st
import pandas as pd
import random
import plotly.express as px
from datetime import datetime, timedelta

def generate_dummy_data():
    """Menghasilkan dataframe berisi 100 baris data transaksi toko elektronik."""
    # Generate 100 tanggal acak dalam 3 bulan terakhir
    base_date = datetime.today()
    dates = [base_date - timedelta(days=random.randint(0, 90)) for _ in range(100)]
    
    kategori_list = ['Laptop', 'HP', 'Aksesoris']
    produk_dict = {
        'Laptop': ['MacBook Pro 14', 'Dell XPS 13', 'Lenovo ThinkPad', 'Asus ROG Zephyrus'],
        'HP': ['iPhone 15 Pro', 'Samsung Galaxy S24', 'Xiaomi 14', 'Google Pixel 8'],
        'Aksesoris': ['Mouse Logitech Wireless', 'Keyboard Mechanical Keychron', 'Headset Sony Bluetooth', 'Charger Anker 65W']
    }
    
    data = []
    for i in range(100):
        kategori = random.choice(kategori_list)
        produk = random.choice(produk_dict[kategori])
        
        # Harga disesuaikan berdasarkan kategori
        if kategori == 'Laptop':
            harga = random.randint(10000000, 35000000)
        elif kategori == 'HP':
            harga = random.randint(7000000, 22000000)
        else:
            harga = random.randint(150000, 2500000)
            
        # Membulatkan harga agar terlihat lebih realistis (kelipatan 10.000)
        harga = round(harga, -4) 
        
        jumlah = random.randint(1, 15)
        # Menghitung Total Pendapatan
        total_pendapatan = harga * jumlah
        
        data.append({
            'Tanggal': dates[i].date(),
            'Kategori': kategori,
            'Produk': produk,
            'Harga': harga,
            'Jumlah Terjual': jumlah,
            'Total Pendapatan': total_pendapatan
        })
        
    df = pd.DataFrame(data)
    # Urutkan dataframe berdasarkan tanggal (lama ke baru)
    df = df.sort_values(by='Tanggal').reset_index(drop=True)
    return df

# Konfigurasi halaman (Opsional: agar layout lebih lebar dan rapi)
st.set_page_config(page_title="Dashboard Penjualan", layout="wide")

# Menambahkan Judul sesuai permintaan
st.title("Sales Data Overview")

# Membuat data dummy dan menyimpannya di cache agar tidak berubah-ubah saat re-render
@st.cache_data
def load_data():
    return generate_dummy_data()

df_sales = load_data()

# --- SIDEBAR & FILTER ---
st.sidebar.header("Filter Data")

# Ambil daftar kategori unik dari dataframe
kategori_unik = df_sales['Kategori'].unique()

# Membuat multiselect box, defaultnya semua kategori terpilih
kategori_pilihan = st.sidebar.multiselect(
    "Pilih Kategori:",
    options=kategori_unik,
    default=kategori_unik
)

# Filter data berdasarkan pilihan
# Jika tidak ada yang dipilih, tampilan tabel akan kosong (hanya header)
df_filtered = df_sales[df_sales['Kategori'].isin(kategori_pilihan)]

# --- MENAMPILKAN DATA ---
st.subheader("Visualisasi Data")

# Membagi layar menjadi 2 kolom untuk grafik
col1, col2 = st.columns(2)

with col1:
    # Grafik 1: Tren Total Pendapatan per Tanggal
    # Kelompokkan data berdasarkan tanggal karena bisa ada lebih dari 1 transaksi di hari yang sama
    df_trend = df_filtered.groupby('Tanggal')['Total Pendapatan'].sum().reset_index()
    fig_line = px.line(
        df_trend, 
        x='Tanggal', 
        y='Total Pendapatan', 
        title='Tren Total Pendapatan',
        markers=True
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    # Grafik 2: Total Jumlah Terjual per Kategori
    # Kelompokkan data berdasarkan kategori
    df_kategori = df_filtered.groupby('Kategori')['Jumlah Terjual'].sum().reset_index()
    fig_bar = px.bar(
        df_kategori, 
        x='Kategori', 
        y='Jumlah Terjual', 
        title='Total Produk Terjual per Kategori',
        color='Kategori'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Menambahkan subheader sebelum tabel
st.subheader("Detail Transaksi")

# Menampilkan dataframe yang sudah difilter
st.dataframe(
    df_filtered, 
    use_container_width=True,
    column_config={
        "Tanggal": st.column_config.DateColumn("Tanggal"),
        "Harga": st.column_config.NumberColumn("Harga", format="Rp %d"),
        "Jumlah Terjual": st.column_config.NumberColumn("Jumlah Terjual"),
        "Total Pendapatan": st.column_config.NumberColumn("Total Pendapatan", format="Rp %d")
    }
)
