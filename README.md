# Exchange Rate and Bitmonedero ETL Pipeline

Este proyecto utiliza Apache Airflow para extraer, transformar y cargar datos de tasas de cambio y precios de Bitmonedero. También se generan alertas basadas en tendencias detectadas en los datos.

## Descripción

El pipeline ETL (Extract, Transform, Load) está diseñado para:
1. Validar credenciales.
2. Extraer datos de APIs de tasas de cambio y Bitmonedero.
3. Transformar y limpiar los datos extraídos.
4. Cargar los datos limpios en una base de datos o almacenamiento específico.
5. Enviar alertas por correo electrónico si se detectan tendencias significativas en los datos.

## Estructura del Proyecto
.
├── dags
│ ├── my_dag.py
│ ├── modules
│ │ ├── validate_credentials.py
│ │ ├── extract_data.py
│ │ ├── data_transformation.py
│ │ ├── clean_and_transformation.py
│ │ ├── load_data.py
│ │ ├── alert_email.py
│ └── parameters.py
├── Dockerfile
├── docker-compose.yml
└── README.md


### Descripción de los Archivos Principales

- `dags/my_dag.py`: Define el pipeline ETL en Airflow.
- `modules/validate_credentials.py`: Contiene funciones para validar credenciales.
- `modules/extract_data.py`: Contiene funciones para extraer datos de las APIs.
- `modules/data_transformation.py`: Contiene funciones para transformar los datos extraídos.
- `modules/clean_and_transformation.py`: Contiene funciones para limpiar los datos transformados.
- `modules/load_data.py`: Contiene funciones para cargar los datos en la base de datos o almacenamiento.
- `modules/alert_email.py`: Contiene funciones para enviar alertas por correo electrónico.
- `parameters.py`: Contiene parámetros y configuraciones globales.
- `Dockerfile`: Define la configuración de Docker para el entorno de Airflow.
- `docker-compose.yml`: Define la configuración de Docker Compose para levantar el entorno de Airflow.

## Requisitos

- Docker
- Docker Compose

## Configuración del Entorno

1. Clona este repositorio:

   ```sh
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
2. Copia y renombra el archivo de ejemplo .env.example a .env y configura las variables de entorno necesarias.

3. Levanta los contenedores de Docker:
   docker-compose up -d
4. Inicializa la base de datos de Airflow (si es necesario):
   docker-compose exec webserver airflow db init
5. Crea un usuario administrador para Airflow:
   docker-compose exec webserver airflow users create \
    --username admin \
    --firstname Firstname \
    --lastname Lastname \
    --role Admin \
    --email admin@example.com
   
### Uso
Accede a la interfaz web de Airflow en http://localhost:8080.

En la interfaz de Airflow, habilita y ejecuta el DAG exchange_rate_dag.

### Tareas en el DAG
#### extract_exchange_data: Extrae datos de tasas de cambio desde la API.

#### extract_bitmonedero_data: Extrae datos de Bitmonedero desde la API.

#### transform_and_clean_exchange_data: Transforma y limpia los datos de tasas de cambio.

#### transform_and_clean_bitmonedero_data: Transforma y limpia los datos de Bitmonedero.

#### load_exchange_data: Carga los datos de tasas de cambio limpios.

#### load_bitmonedero_data: Carga los datos de Bitmonedero limpios.

#### alert_email_exchange: Envía alertas por correo electrónico para tasas de cambio.

#### alert_email_bitmonedero: Envía alertas por correo electrónico para Bitmonedero.

