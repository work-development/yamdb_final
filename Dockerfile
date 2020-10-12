FROM python:3.8

WORKDIR code

COPY ./requirements.txt /code

RUN pip install -r /code/requirements.txt

COPY . code

WORKDIR code

CMD gunicorn api_yamdb.wsgi:application --bind 8000