FROM python:3.8-slim-buster
RUN apt-get update && apt-get install wget curl -y

WORKDIR /app

RUN curl 'https://raw.githubusercontent.com/newrelic/newrelic-python-agent/main/newrelic/newrelic.ini' --output newrelic.ini
COPY . . 

ENV FILTER_RULE = ${FILTER_RULE}

RUN pip3 install --no-cache-dir poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install

CMD ["poetry","run","python3","-m","app"]