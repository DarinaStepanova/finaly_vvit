FROM python:3.10
WORKDIR /app

COPY . /app

RUN apt-get update
RUN apt-get install docker-compose -y
RUN pip install -r requirements.txt

EXPOSE 8888 8889 5433 5050

CMD ["docker-compose", "up", "-d", "docker-compose.yaml"]
CMD ["python3", "app.py"]
