import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

data = pd.read_csv("DailyDelhiClimateTrain.csv")
print(data.head())

print(data.describe())

print(data.info())


data = pd.read_csv("DailyDelhiClimateTrain.csv")# Veriyi yükle

# Histogram oluştur
figure = px.histogram(data, x="meantemp", 
                      title='Distribution of Mean Temperature in Delhi',
                      color_discrete_sequence=['green'],
                      opacity=0.7,  # Çubukların saydamlığı
                      nbins=50,  # Çubuk sayısı
                      barmode='overlay'  # Çubuk modu
                     )


figure.update_traces(marker=dict(line=dict(width=0.5, color='black')))# Çubuk kenarlıklarını belirginleştir

# Grafik stilini ayarla
figure.update_layout(
    plot_bgcolor='rgba(255, 255, 255, 0)',  # Arka plan rengi
    width=800,  # Genişlik
    height=600,  # Yükseklik
    xaxis=dict(title='Mean Temperature (°C)'),  # X ekseninin başlığı
    yaxis=dict(title='Frequency'),  # Y ekseninin başlığı
    font=dict(color='black')  # Yazı rengi
)

figure.show()

figure = px.line(data, x="date", 
                 y="humidity", 
                 title='Humidity in Delhi Over the Years',
                 color_discrete_sequence=['green'])

figure.update_layout(
    plot_bgcolor='lightgreen',  # Arka plan rengi
    width=900,  # Genişlik
    height=700  # Yükseklik
)
figure.show()

figure = px.line(data, x="date", 
                 y="wind_speed", 
                 title='Wind Speed in Delhi Over the Years',
                 color_discrete_sequence=['green'])

figure.update_layout(
    plot_bgcolor='lightgreen',  
    width=900,  
    height=600  
)
figure.show()

colorscale = [(0, "green"), (1, "lightgreen")]

figure = px.scatter(data_frame=data, x="humidity",
                    y="meantemp", size="meantemp", 
                    trendline="ols", 
                    title="Nem ve Ortalama Sıcaklık Arasındaki İlişki",
                    labels={"humidity": "Nem (%)", "meantemp": "Ortalama Sıcaklık (°C)"},
                    color_continuous_scale=colorscale)

figure = px.scatter(data_frame=data, x="humidity", y="meantemp",
                 title="Nem ve Ortalama Sıcaklık Arasındaki İlişki",
                 labels={"humidity": "Nem (%)", "meantemp": "Ortalama Sıcaklık (°C)"},
                 trendline="ols")


figure.show()

# data["date"] = pd.to_datetime(data["date"], format = '%Y-%m-%d')
# data['year'] = data['date'].dt.year
# data["month"] = data["date"].dt.month
# print(data.head())

# plt.style.use('fivethirtyeight')
# plt.figure(figsize=(15, 10))
# plt.title("Temperature Change in Delhi Over the Years")
# sns.lineplot(data = data, x='month', y='meantemp', hue='year')
# plt.show()
# Tarih sütununu datetime'a dönüştür

data["date"] = pd.to_datetime(data["date"], format='%Y-%m-%d')
data["month"] = data["date"].dt.month

# Ay sırasına göre ortalama sıcaklığı hesapla
monthly_mean_temp = data.groupby("month")["meantemp"].mean()

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

labels = months
sizes = monthly_mean_temp
explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)  

plt.figure(figsize=(8, 8))
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('Average Temperature by Month')
plt.axis('equal') 
plt.show()

forecast_data = data.rename(columns = {"date": "ds", 
                                       "meantemp": "y"})
print(forecast_data)

from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
model = Prophet()
model.fit(forecast_data)
forecasts = model.make_future_dataframe(periods=365)
predictions = model.predict(forecasts)
plot_plotly(model, predictions)