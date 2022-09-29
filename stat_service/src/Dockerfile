FROM python:3.8.5

WORKDIR /usr/app

RUN pip install --upgrade pip --no-cache-dir
RUN apt-get update && apt-get -y dist-upgrade

COPY ./src/requirements.txt ./
COPY ./src/fake_film_db.txt ./
COPY ./src/fake_genre_db.txt ./

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["./entrypoint.sh"]