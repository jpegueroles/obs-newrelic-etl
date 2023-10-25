# ccom-obs-nr-etl


# Ejecutar en local

## Preparación ambiente

``` sh
poetry install
```

Si utiliza visual studio code debe configurar el interprete de python y seleccionar el que diga Poetry.

Debes configurar tus credenciales programaticas de AWS para poder almacenar el fichero en el bucket.

Se debe setear ciertos export:

``` sh
export NR_ACCOUNT_ID=your_New_Relic_account_id
export NEW_RELIC_APP_NAME="obs-nr-etl-localhost"
export AWS_DEFAULT_REGION="us-east-1"
export NR_API_KEY="your_api_key"
export AWS_BUCKET_NAME="your_bucket_name"
```

Si vas a crear una imagen de docker para contenerizar el codigo, el archivo .ini no es necesario tenerlo ya que al ejecutarse el contendor este genera el archivo .ini

## Getting started

