FROM python:3.8.5

WORKDIR /usr/app

RUN pip install --upgrade pip --no-cache-dir
RUN apt-get update && apt-get -y dist-upgrade

COPY ./tests/requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["./entrypoint.sh"]