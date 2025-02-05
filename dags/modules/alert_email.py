import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)


def send_email(subject, body):
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL') 
    password = os.getenv('PASSWORD_EMAIL')  
       
    # Crear el objeto del mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Agregar el cuerpo del mensaje al email
    msg.attach(MIMEText(body, 'plain'))

    # Crear la conexión segura con el servidor y enviar el email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Correo enviado exitosamente!")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def check_for_trend(data, previous_data_list, trend_length, currency_column='currency', rate_column='rate'):
    """
    Comprueba una tendencia de aumento o disminución en los datos durante un número de días consecutivos.
    Envía alertas si se detecta una tendencia significativa.
    """
    trend_detected = False

    # Filtrar las tasas de cambio (excluyendo BTC si existe en los datos)
    rate_data = data[data[currency_column] != 'BTC']
    btc_data = data[data[currency_column] == 'BTC']

    for _, row in rate_data.iterrows():
        rate_trend = all(row[rate_column] > prev_data[rate_column] for prev_data_list in previous_data_list for prev_data in prev_data_list if prev_data[currency_column] == row[currency_column])
        if rate_trend:
            trend_detected = True
            subject = f"Alerta de Tendencia de Aumento de Tasa de Cambio para {row[currency_column]}"
            body = f"Se ha detectado una tendencia de aumento en la tasa de cambio de {row[currency_column]} durante los últimos {trend_length} días."
            send_email(subject, body)
            print(f"Alerta enviada debido a tendencia de aumento en la tasa de cambio de {row[currency_column]}.")

    if not btc_data.empty:
        btc_trend = all(btc_data[rate_column].values[0] > prev_data[rate_column] for prev_data_list in previous_data_list for prev_data in prev_data_list if prev_data[currency_column] == 'BTC')
        if btc_trend:
            trend_detected = True
            subject = "Alerta de Tendencia de Aumento de Precio BTC"
            body = f"Se ha detectado una tendencia de aumento en el precio de BTC durante los últimos {trend_length} días."
            send_email(subject, body)
            print("Alerta enviada debido a tendencia de aumento en el precio de BTC.")

    if not trend_detected:
        print("No se detectaron tendencias significativas.")