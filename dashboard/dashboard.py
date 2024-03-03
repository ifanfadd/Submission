import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# INPUT DATA
customer_df = pd.read_csv('https://raw.githubusercontent.com/ifanfadd/Submission/main/dashboard/customer_df_new.csv')
orders_df = pd.read_csv('https://raw.githubusercontent.com/ifanfadd/Submission/main/dashboard/orders_df_new.csv')
payment_df = pd.read_csv('https://raw.githubusercontent.com/ifanfadd/Submission/main/dashboard/payment_df_new.csv')

# EDA
# MENGELOMPOKKAN DATA CUSTOMER, LALU HITUNG ORDER_ID PER CUSTOMER (BANYAK ORDERAN)
orders_per_customer = orders_df.groupby('customer_id')['order_id'].count().reset_index()
# MEMBUAT NAMA KOLOM
orders_per_customer.columns = ['customer_id', 'total_orders']
# GABUNGKAN ORDER PER CUSTOMER DENGAN DATA CUSTOMER (AMBIL FEATURE NEGARA BAGIAN/STATE)
merged_df = pd.merge(orders_per_customer, customer_df[['customer_id', 'customer_state']], on='customer_id', how='left')
# MENGELOMPOKKAN BERADASARKAN CUSTOMER STATE DAN HITUNG TOTAL ORDERS
orders_per_state = merged_df.groupby('customer_state')['total_orders'].sum().reset_index()
# MENGURUTKAN ORDER PER STATE DARI BANYAKNYA ORDER
orders_per_state = orders_per_state.sort_values(by='total_orders', ascending=False)

# MENGHITUNG DISTRIBUSI BERDASARKAN JENIS PEMBAYARAN
payment_distribution = payment_df['payment_type'].value_counts()

st.header('Proyek Analisis Data Dashboard :sparkles:')

with st.sidebar:
    # Menambahkan gambar
    st.image("https://static.vecteezy.com/system/resources/previews/000/483/336/original/shopping-e-commerce-concept-isometric-poster-vector.jpg")
    st.subheader("Ifan Fadilah at Bangkit Academy")
    st.write("Pada proyek kali ini merupakan analisis data menggunakan dataset e-commerce")
tab1, tab2 = st.tabs(["Tab 1","Tab 2"])

with tab1 :
    st.subheader("Distribusi Customers Berdasarkan Wilayah")
    #VISUALISASI
    bar_chart_data = orders_per_state
    fig_bar, ax_bar = plt.subplots(figsize=(12, 6))
    ax_bar.bar(bar_chart_data['customer_state'], bar_chart_data['total_orders'], color='skyblue', edgecolor='black')
    ax_bar.set_title('Total Orders per State')
    ax_bar.set_xlabel('Customer State')
    ax_bar.set_ylabel('Total Orders')
    ax_bar.set_xticks(bar_chart_data['customer_state'])
    ax_bar.tick_params(axis='x', rotation=45, labelrotation=45)  # Use labelrotation instead of ha
    ax_bar.grid(axis='y', linestyle='--', alpha=0.7)

    # DISPLAY
    st.pyplot(fig_bar)

    with st.expander("Lihat Penjelasan"):
        st.write("Distribusi pemesanan berdasarkan lokasi pemesanan terbilang cukup tidak merata, pemesanan terbanyak ada pada Sao Paulo dengan nilai lebih dari 40000 pemesanan, sedangkan state lain terhitung hanya dibawah 15000 pemesanan dari total 99441 pemesanan yang  dilakukan. Dapat disimpulkan Sao Paulo merupakan state dengan customer terbanyak.")

with tab2 :
    st.subheader("Distribusi Pesanan Berdasarkan Tipe Pembayaran")

    # VISUALISASI
    pie_chart_data = payment_distribution
    fig_pie, ax_pie = plt.subplots(figsize=(10, 8))
    colors = ['skyblue', 'lightgreen', 'lightcoral', 'gold', 'lightpink']
    wedges, texts, autotexts = ax_pie.pie(pie_chart_data, startangle=90, colors=colors, wedgeprops=dict(width=0.3, edgecolor='w'),
                                    autopct='', pctdistance=0.85)

    legend_labels = [f"{label}: {percentage:.1f}% ({count})" for label, percentage, count in
                    zip(pie_chart_data.index, (pie_chart_data / pie_chart_data.sum()) * 100, pie_chart_data)]

    ax_pie.legend(wedges, legend_labels, title='Payment Types', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

    fig_pie.subplots_adjust(left=0.0, right=0.55)
    ax_pie.set_title('Distribution of Payment Types')

    # DISPLAY
    st.pyplot(fig_pie)

    with st.expander("lihat penjelasan"):
        st.write("Distribusi pemesanan berdasarkan tipe pembayaran juga tidak merata, customer yang melakukan pembayaran menggunakan credit card ada sekitar 73% dari 103877 pembayaran yang telah dilakukan atau sekitar . Dapat disimpulkan bahwa pembayaran credit card merupakan  tipe pembayaran yang cukup disukai oleh customer.")