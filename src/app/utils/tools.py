import os
import logging
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from configparser import ConfigParser
from .nerdgraph_tools import *
from .aws_s3 import *

logger = logging.getLogger()

def mod_ini(license_key,app_name):
    # Instantiate
    config = ConfigParser()

    # Obtén la ruta al directorio actual donde se encuentra tools.py
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construye la ruta al archivo de configuración usando una ruta relativa
    config_file_path = os.path.join(script_dir, "../../../newrelic.ini")
    
    # Parse existing file
    config.read(config_file_path)

    # Update existing value
    config.set('newrelic', 'license_key', license_key)
    config.set('newrelic', 'app_name', app_name)

    # Save to a file
    with open(config_file_path, 'w') as configfile:
        config.write(configfile) 

########################################
def transform_data_example(data):
    # Ejemplo de escritura de datos en Parquet FORMATO TBD
    table = pa.Table.from_pandas(data)  
    with pa.OSFile('data.parquet', 'wb') as sink:
        with pa.RecordBatchFileWriter(sink, table.schema) as writer:
            writer.write_table(table)

    table = pa.Table.from_pandas(data)  # 'data' es tu conjunto de datos
    logger.info(table)
    local_file_path = 'data.parquet'

#########################################
def transform_data(data):

    # Extraer las series temporales
    time_series = data.get("timeSeries", [])

    # Crear una lista para cada columna del DataFrame
    begin_time = []
    end_time = []
    average_values = []

    for entry in time_series:
        begin_time.append(entry["beginTimeSeconds"])
        end_time.append(entry["endTimeSeconds"])
        average_values.append(entry["results"][0]["average"])

    # Crear un DataFrame de Pandas
    df = pd.DataFrame({
        "beginTime": begin_time,
        "endTime": end_time,
        "average": average_values
    })

    # Crear una tabla PyArrow a partir del DataFrame
    table = pa.Table.from_pandas(df)

    # Escribir la tabla en un archivo Parquet
    output_file = 'metric_data.parquet'
    pq.write_table(table, output_file)
    
    return output_file

########################################
def save_file(file_name, bucket_name):
    prefix = 'newrelic_data/'

    putS3obj(bucket_name, prefix,file_name)

    pass
########################################
