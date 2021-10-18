# Dockerfile
FROM python:3.9-slim
LABEL maintainer="jlatorre@irontec.com"
ENV PROJECT_ROOT /app
WORKDIR $PROJECT_ROOT
RUN apt update && apt install -y pipenv default-libmysqlclient-dev libjpeg-dev wget git
COPY install-wkhtmltopdf.sh /app/
RUN sh /app/install-wkhtmltopdf.sh
RUN pip install mysqlclient  
COPY requirements* /app/
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000