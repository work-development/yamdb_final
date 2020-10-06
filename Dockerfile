
FROM python:3.8

WORKDIR /code

COPY requirements.txt /code

COPY static /var/lib/

RUN pip install -r /code/requirements.txt

COPY . /code

WORKDIR /code

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000








