from modules.data_from_api import exchange_rate, bitmonedero_data

def extract_exchange_data(api_url):
    data = exchange_rate(api_url)
    return data


def extract_bitmonedero_data():
    return bitmonedero_data()
