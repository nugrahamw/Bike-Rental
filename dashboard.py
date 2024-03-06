import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_color_codes('bright')
import streamlit as st

day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

season_labels = {
    1 : 'springer',
    2 : 'summer',
    3 : 'fall',
    4 : 'winter'
}

weather_labels = {
    1 : 'Cerah',
    2 : 'Berawan',
    3 : 'HujanRingan',
    4 : 'HujanLebat'
}


# function for denormalization temp and atemp variable
def denorm(y, t_min, t_max):
    x = y * (t_max - t_min) + t_min
    return x

# change dtype of dteday from object to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# denormalisasi variabel temp
day_df['temp'] = denorm(day_df['temp'], -8, 39)
hour_df['temp'] = denorm(hour_df['temp'], -8, 39)

# denormalisasi variabel atemp
day_df['atemp'] = denorm(day_df['atemp'], -16, 50)
hour_df['atemp'] = denorm(hour_df['atemp'], -16, 50)

# denormalisasi variabel hum
day_df['hum'] = day_df['hum']*100
hour_df['hum'] = hour_df['hum']*100

# denormalisasi variabel windspeed
day_df['windspeed'] = day_df['windspeed']*67
hour_df['windspeed'] = day_df['windspeed']*67

# change format variable to real data
day_df['season'] = day_df['season'].map(season_labels)
hour_df['season'] = hour_df['season'].map(season_labels)
day_df['weathersit'] = day_df['weathersit'].map(weather_labels)
hour_df['weathersit'] = hour_df['weathersit'].map(weather_labels)

# The Dashboard
min_date = day_df['dteday'].dt.date.min()
max_date = day_df['dteday'].dt.date.max()

with st.sidebar:
    st.image('bike.png', use_column_width = True, caption = 'Bike Sharing') 
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Interval Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

# create dataframe based the time
main_day_df = day_df[(day_df['dteday'] >= str(start_date)) & (day_df['dteday'] <= str(end_date))]
main_hour_df = hour_df[(hour_df['dteday'] >= str(start_date)) & (hour_df['dteday'] <= str(end_date))]

st.header('Bicycle Rental Dashboard 🚲')

st.subheader('Daily Rental')
total_rent_perhour = main_hour_df.cnt.sum()/len(main_day_df)
casual_rent_perhour = main_hour_df.casual.sum()/len(main_day_df)
registered_rent_perhour = main_hour_df.registered.sum()/len(main_day_df)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Average Daily Casual User", value=round(casual_rent_perhour, 2))
with col2:
    st.metric("Average Daily Registered User", value=round(registered_rent_perhour, 2))
with col3:
    st.metric("Average Daily Total User", value=round(total_rent_perhour, 2))

st.subheader('Pengaruh Kecepatan Angin Terhadap Jumlah Penyewaan') #=================================================
plt.figure(figsize = (35,15))
# plt.subplot(2,1,1)
plt.scatter(day_df['windspeed'], day_df['cnt'], color='blue', alpha=0.6, s=50)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Kecepatan Angin', fontsize=20)
plt.ylabel('Jumlah Penyewa', fontsize=20)
plt.legend(['Count'], fontsize=20)
st.pyplot(plt.gcf())

st.subheader('Rata-Rata Penyewaan Per-Harinya') #=================================================
plt.figure(figsize = (15,7))
daily_rentals_by_day = day_df.groupby('weekday')[['casual', 'registered']].mean().reset_index()

# Mengubah angka hari menjadi label yang sesuai
weekday_map = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
daily_rentals_by_day['weekday'] = daily_rentals_by_day['weekday'].map(weekday_map)

# Plot pengaruh hari terhadap jumlah penyewa
plt.figure(figsize=(10, 6))
sns.barplot(data=daily_rentals_by_day, x='weekday', y='casual', color='blue', label='Casual')
sns.barplot(data=daily_rentals_by_day, x='weekday', y='registered', color='skyblue', label='Registered', alpha=0.7)

plt.xlabel('Hari')
plt.ylabel('Rata-Rata Peminjaman')
plt.xticks(fontsize = 10)
plt.gca().ticklabel_format(style = 'plain', axis = 'y')
plt.yticks(fontsize = 10)
st.pyplot(plt)

st.subheader('Perbandingan Pengguna Terdaftar dan Pengguna Casual?') #=================================================
plt.figure(figsize = (15,7))
sns.set(style="whitegrid")

total_casual = sum(day_df['casual'])
total_registered = sum(day_df['registered'])
data = [total_casual, total_registered]
labels = ['Casual', 'Registered']

colors = ['#3366FF','#FF5733']

plt.pie(data, labels=labels, autopct='%1.1f%%', wedgeprops=dict(width=0.4, edgecolor='b'), colors=colors)

st.pyplot(plt)

