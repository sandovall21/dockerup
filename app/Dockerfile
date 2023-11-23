FROM python:3.9

EXPOSE 5000

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install Flask
RUN pip install mysql-connector

CMD python app.py