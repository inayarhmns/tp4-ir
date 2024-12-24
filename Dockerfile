FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

RUN python3 manage.py collectstatic --no-input --clear

CMD ["gunicorn", "tp4.wsgi:application", "--bind", "0.0.0.0:8000"]
