FROM python:3.8.13
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN python manage.py migrate