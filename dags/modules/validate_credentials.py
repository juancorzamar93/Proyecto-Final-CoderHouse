from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)


def validate_credentials():
    credentials = {
        "API_KEY": os.getenv('API_KEY'),
        "REDSHIFT_USERNAME": os.getenv('REDSHIFT_USERNAME'),
        "REDSHIFT_PASSWORD": os.getenv('REDSHIFT_PASSWORD'),
        "REDSHIFT_HOST": os.getenv('REDSHIFT_HOST').replace('http://', ''),
        "REDSHIFT_DB": os.getenv('REDSHIFT_DB'),
        "REDSHIFT_PORT": os.getenv('REDSHIFT_PORT')
    }

    for key, value in credentials.items():
        if not value or value == '':
            print(f"Error: {key} is not set properly.")
            return False

    print("All credentials are set properly.")
    return True
