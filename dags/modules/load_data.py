from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from parameters import REDSHIFT_USERNAME, REDSHIFT_PASSWORD, REDSHIFT_HOST, REDSHIFT_DB, REDSHIFT_PORT, REDSHIFT_TABLE

def load_data(df):
    try:
        # Crear el string de conexión
        conn_str = f'postgresql+psycopg2://{REDSHIFT_USERNAME}:{REDSHIFT_PASSWORD}@{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}'
        
        # Crear el motor de SQLAlchemy
        engine = create_engine(conn_str)

        # Conectar al motor
        with engine.connect() as connection:
            # Insertar datos en la tabla
            df.to_sql(REDSHIFT_TABLE, con=connection, if_exists='append', index=False)

        print("Datos cargados exitosamente en Redshift")
    
    except SQLAlchemyError as e:
        print(f"Error al cargar los datos de exchange rate en Redshift: {e}")

    except Exception as e:
        print(f"Error general: {e}")


def load_bitmonedero_data(df):
    try:
        conn_str = f'postgresql+psycopg2://{REDSHIFT_USERNAME}:{REDSHIFT_PASSWORD}@{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}'
        engine = create_engine(conn_str)
        with engine.connect() as connection:
            df.to_sql(REDSHIFT_TABLE, con=connection, if_exists='append', index=False)
        print("Datos de Bitmonedero cargados exitosamente en Redshift")
    except SQLAlchemyError as e:
        print(f"Error al cargar datos de Bitmonedero en Redshift: {e}")


