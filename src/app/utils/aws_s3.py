import csv
import logging
import boto3
import datetime

from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger_error = logging.getLogger('errores')
logger_error.setLevel(logging.ERROR)

def getS3obj(bucket_name, file_name):
    white_list = list()
    try:
        s3 = boto3.client('s3',region_name='us-east-1')
        obj = s3.get_object(Bucket=bucket_name, Key=file_name)

        data = obj['Body'].read().decode('utf-8').splitlines() 
        records = csv.reader(data)
        headers = next(records)
        for eachRecord in records:
            white_list.extend(eachRecord)
        
        return white_list
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            logger_error.error(f"El archivo '{file_name}' no existe en el bucket '{bucket_name}'.")
        else:
            logger_error.error(f"Error al leer el archivo desde S3: {str(e)}")
    except NoCredentialsError as e:
        logger_error.error("No se encontraron credenciales de AWS configuradas.")
    except Exception as e:
        logger_error.error(f"Se produjo una excepción al leer el archivo desde S3: {str(e)}")

def putS3obj(bucket_name, prefix, file_name):   # Sube los datos a S3
    try:
        s3 = boto3.client('s3',region_name='us-east-1')
        s3.upload_file(file_name, bucket_name, f'{prefix}{datetime.date.today()}/{file_name}')
        logger.info(f'file uploaded to: {prefix}{datetime.date.today()}/{file_name}')
    except NoCredentialsError:
        logger_error.error("No se encontraron credenciales para acceder a S3. Verifica tu configuración de AWS.")
    except PartialCredentialsError:
        logger_error.error("Las credenciales proporcionadas son parciales o inválidas. Verifica tus credenciales de AWS.")
    except Exception as e:
        logger_error.error(f"Ocurrió un error inesperado: {str(e)}")
