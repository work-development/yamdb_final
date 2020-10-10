FROM python:3.8

WORKDIR code

COPY ./requirements.txt /code

RUN pip install -r /code/requirements.txt

COPY . code

WORKDIR code

CMD gunicorn api_yamdb.wsgiapplication --bind 0.0.0.08000