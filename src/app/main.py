import json
import boto3
import newrelic.agent
import logging

from .utils.tools import *

logger = logging.getLogger()
logHandler = logging.StreamHandler()
logger.setLevel(logging.INFO)
logger.addHandler(logHandler)

#configure boto3
boto3.setup_default_session(region_name='us-east-1')

#setear nombre del secret de la licencia a usar para NR y otras vars necesarias
bucket_name = os.environ["AWS_BUCKET_NAME"]

#set newrelic credentials 
user_key = os.environ["NR_API_KEY"]
acc_id = os.environ["NR_ACCOUNT_ID"]

#modify file: newrelic.ini
mod_ini(os.environ["NEW_RELIC_LICENSE_KEY"],os.environ["NEW_RELIC_APP_NAME"])
newrelic.agent.initialize(config_file='newrelic.ini')
newrelic.agent.set_background_task(True)


# Función para extraer datos de New Relic y almacenarlos en S3
@newrelic.agent.background_task(name="main", group="OBSERVABILITY")
def main():    
    guid = "MzkwMDczM3xBUE18QVBQTElDQVRJT058MTUxNzIxMTQxOA"

    # Realiza consultas a NerdGraph aquí y procesa los resultados
    logger.info(f'acc: {acc_id}')
    logger.info(f'user_key: {user_key}')
    logger.info(f'guid: {guid}')
    data = getData(user_key, acc_id, guid)
    # trasformara el rawResponse en parquet, lo almacenará en local y transfiere a bucket
    save_file(transform_data(data), bucket_name)
    

if __name__ == '__main__':
    main()