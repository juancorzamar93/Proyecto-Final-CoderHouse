from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
from modules.validate_credentials import validate_credentials
from modules.extract_data import extract_exchange_data as api_extract_exchange_data
from modules.extract_data import extract_bitmonedero_data as API_extract_bitmonedero_data
from modules.data_transformation import transform_data, transform_bitmonedero_data
from modules.clean_and_transformation import clean_data
from modules.load_data import load_data as load_ex_data, load_bitmonedero_data as load_bit_data
from modules.alert_email import send_email, check_for_trend
from parameters import API_URL
from dotenv import load_dotenv
import json


load_dotenv()

def validate_credentials():
    if not validate_credentials():
        raise ValueError("Invalid credentials. Exiting...")

def extract_exchange_data(**kwargs):
    data = api_extract_exchange_data(API_URL)
    if data:
        kwargs['ti'].xcom_push(key='raw_exchange_data', value=data)
    else:
        raise ValueError("No data extracted from Exchange API.")

def transform_and_clean_exchange_data(**kwargs):
    ti = kwargs['ti']
    raw_data = ti.xcom_pull(task_ids='extract_exchange_data', key='raw_exchange_data')
    
    # Transformar y limpiar datos
    transformed_data = transform_data(raw_data)
    cleaned_data = clean_data(transformed_data)
    
    ti.xcom_push(key='cleaned_exchange_data', value=cleaned_data)

def load_exchange_data(**kwargs):
    ti = kwargs['ti']
    cleaned_data = ti.xcom_pull(task_ids='transform_and_clean_exchange_data', key='cleaned_exchange_data')
    load_ex_data(cleaned_data)


def extract_bitmonedero_data(**kwargs):
    data = API_extract_bitmonedero_data()
    if data:
        kwargs['ti'].xcom_push(key='bitmonedero_data', value=data)
    else:
        raise ValueError("No data extracted from Bitmonedero.")

def transform_and_clean_bitmonedero_data(**kwargs):
    ti = kwargs['ti']
    raw_data = ti.xcom_pull(task_ids='extract_bitmonedero_data', key='bitmonedero_data')
    transformed_data = transform_bitmonedero_data(raw_data)
    cleaned_data = clean_data(transformed_data)
    ti.xcom_push(key='cleaned_bitmonedero_data', value=cleaned_data)

def load_bitmonedero_data(**kwargs):
    ti = kwargs['ti']
    cleaned_data = ti.xcom_pull(task_ids='transform_and_clean_bitmonedero_data', key='cleaned_bitmonedero_data')
    load_bit_data(cleaned_data)


# def send_alerts(**kwargs):
#     ti = kwargs['ti']
#     cleaned_data = ti.xcom_pull(task_ids='extract_and_transform_data', key='cleaned_data')
    
#     # Supongamos que los datos vienen en un formato adecuado, o necesitas transformarlos aquí
#     rate_threshold = float(Variable.get("rate_threshold", default_var=0.001))  # Ejemplo de umbral
#     btc_price_threshold = float(Variable.get("btc_price_threshold", default_var=100000))
    
#     check_for_alerts(cleaned_data, rate_threshold, btc_price_threshold) 

# def send_alerts(**kwargs):
#     ti = kwargs['ti']
#     cleaned_data = ti.xcom_pull(task_ids='load_exchange_data', key='cleaned_exchange_data')
    
#     previous_data_list_str = Variable.get("previous_data_list", default_var="[]")
#     previous_data_list = json.loads(previous_data_list_str)
    
#     trend_length = 3
#     if len(previous_data_list) >= trend_length:
#         check_for_trend(cleaned_data, previous_data_list[-trend_length:], trend_length)
#         previous_data_list.append(cleaned_data)
#         previous_data_list = previous_data_list[-trend_length:]
#     else:
#         previous_data_list.append(cleaned_data)

#     # Actualizar la variable con los datos más recientes
#     Variable.set("previous_data_list", json.dumps(previous_data_list))

# def send_alerts(**kwargs):
#     ti = kwargs['ti']
#     cleaned_data = ti.xcom_pull(task_ids='load_exchange_data', key='cleaned_exchange_data')
#     cleaned_data_bit = ti.xcom_pull(task_ids='load_bitmonedero_data', key='cleaned_bitmonedero_data')
    
#     # Combinar los datos
#     combined_data = cleaned_data.append(cleaned_data_bit, ignore_index=True)
    
#     previous_data_list_str = Variable.get("previous_data_list", default_var="[]")
#     previous_data_list = json.loads(previous_data_list_str)
    
#     trend_length = 1 # dia o dias para comparar el dia actual con el anterior
#     if len(previous_data_list) >= trend_length:
#         check_for_trend(combined_data, previous_data_list[-trend_length:], trend_length)
#         previous_data_list.append(combined_data.to_dict('records'))
#         previous_data_list = previous_data_list[-trend_length:]
#     else:
#         previous_data_list.append(combined_data.to_dict('records'))

#     # Actualizar la variable con los datos más recientes
#     Variable.set("previous_data_list", json.dumps(previous_data_list))

def send_alerts(**kwargs):
    ti = kwargs['ti']
    cleaned_data = ti.xcom_pull(task_ids='load_exchange_data', key='cleaned_exchange_data')
    cleaned_data_bit = ti.xcom_pull(task_ids='load_bitmonedero_data', key='cleaned_bitmonedero_data')
    
    # Comprobaciones para cleaned_data y cleaned_data_bit
    if cleaned_data is None:
        error_message = "Error: cleaned_data is None."
        print(error_message)
        send_email("ETL Failure Alert", error_message)
        raise ValueError(error_message)
    elif cleaned_data_bit is None:
        error_message = "Error: cleaned_data_bit is None."
        print(error_message)
        send_email("ETL Failure Alert", error_message)
        raise ValueError(error_message)
    
    # Combinar los datos
    combined_data = cleaned_data.append(cleaned_data_bit, ignore_index=True)
    
    previous_data_list_str = Variable.get("previous_data_list", default_var="[]")
    previous_data_list = json.loads(previous_data_list_str)
    
    trend_length = 3  # Definir una sola vez aquí
    if len(previous_data_list) >= trend_length:
        check_for_trend(combined_data, previous_data_list[-trend_length:], trend_length)
        previous_data_list.append(combined_data.to_dict('records'))
        previous_data_list = previous_data_list[-trend_length:]
    else:
        previous_data_list.append(combined_data.to_dict('records'))

    # Actualizar la variable con los datos más recientes
    Variable.set("previous_data_list", json.dumps(previous_data_list))



default_args = {
    'owner': 'juan_ml',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'exchange_rate_dag',
    default_args=default_args,
    description='DAG para ETL de tasas de cambio y precios de BTC',
    schedule_interval=timedelta(days=1),
)

with dag:
    
    task_extract_exchange = PythonOperator(
        task_id='extract_exchange_data',
        python_callable=extract_exchange_data, 
        provide_context=True
    )

    task_extract_bitmonedero = PythonOperator(
        task_id='extract_bitmonedero_data',
        python_callable=extract_bitmonedero_data,
        provide_context=True
    )

    task_transform_and_clean_exchange = PythonOperator(
        task_id='transform_and_clean_exchange_data',
        python_callable=transform_and_clean_exchange_data,
        provide_context=True
    )

    task_transform_and_clean_bitmonedero = PythonOperator(
        task_id='transform_and_clean_bitmonedero_data',
        python_callable=transform_and_clean_bitmonedero_data,
        provide_context=True
    )

    task_load_exchange = PythonOperator(
        task_id='load_exchange_data',
        python_callable=load_exchange_data,
        provide_context=True
    )

    task_load_bitmonedero = PythonOperator(
        task_id='load_bitmonedero_data',
        python_callable=load_bitmonedero_data,
        provide_context=True
    )

    task_alert_email = PythonOperator(
        task_id='alert_email',
        python_callable=send_alerts,
        provide_context=True
    )

   
    task_extract_exchange >> task_transform_and_clean_exchange >> task_load_exchange
    task_extract_bitmonedero >> task_transform_and_clean_bitmonedero >> task_load_bitmonedero
    [task_load_exchange, task_load_bitmonedero] >> task_alert_email