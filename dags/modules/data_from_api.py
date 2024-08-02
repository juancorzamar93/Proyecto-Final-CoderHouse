    
import requests
from parameters import API_KEY, BITMONEDERO_API_URL

def exchange_rate(api_url):
    headers = {"apikey": API_KEY}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud a la API: {e}")
        return None

def bitmonedero_data():
    try:
        response = requests.get(BITMONEDERO_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud al API de Bitmonedero: {e}")
        return None
