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

# def check_for_alerts(data, rate_threshold, btc_price_threshold):
#     """
#     Comprueba cambios significativos en el tipo de cambio y en el precio del BTC,
#     y envía alertas de correo electrónico si se superan los umbrales establecidos.
#     """
#     # Alerta para cambio en la tasa de cambio de divisas
#     if data['rate'] > rate_threshold:  #abs(data['rate']) > rate_threshold:
#         subject = "Alerta de Tasa de Cambio"
#         body = f"La tasa de cambio ha variado significativamente: {data['rate']*100}%"
#         send_email(subject, body)
#         print("Alerta enviada debido a cambio significativo en la tasa de cambio.")

#     # Alerta para cambio en el precio de compra de BTC
#     if data['buy_btc_ars'] > btc_price_threshold: #abs(data['buy_btc_ars']) > btc_price_threshold:
#         subject = "Alerta de Precio BTC"
#         body = f"El precio de compra de BTC ha cambiado significativamente, cambio actual: ${data['buy_btc_ars']}"
#         send_email(subject, body)
#         print("Alerta enviada debido a cambio significativo en el precio de BTC.")

#     print("Revisión de alertas completada.")

def check_for_trend(data, previous_data_list, trend_length=3):
    """
    Comprueba una tendencia de aumento o disminución en los datos durante un número de días consecutivos.
    Envía alertas si se detecta una tendencia significativa.
    """
    trend_detected = False

    # Comprueba tendencia en tasa de cambio
    rate_trend = all(data['rate'] > prev_data['rate'] for prev_data in previous_data_list)
    if rate_trend:
        trend_detected = True
        subject = "Alerta de Tendencia de Aumento de Tasa de Cambio"
        body = f"Se ha detectado una tendencia de aumento en la tasa de cambio durante los últimos {trend_length} días."
        send_email(subject, body)
        print("Alerta enviada debido a tendencia de aumento en la tasa de cambio.")

    # Comprueba tendencia en precio de BTC
    btc_trend = all(data['buy_btc_ars'] > prev_data['buy_btc_ars'] for prev_data in previous_data_list)
    if btc_trend:
        trend_detected = True
        subject = "Alerta de Tendencia de Aumento de Precio BTC"
        body = f"Se ha detectado una tendencia de aumento en el precio de BTC durante los últimos {trend_length} días."
        send_email(subject, body)
        print("Alerta enviada debido a tendencia de aumento en el precio de BTC.")

    if not trend_detected:
        print("No se detectaron tendencias significativas.")