FROM python:3.8.5

WORKDIR /usr/app

COPY ./src/requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["./entrypoint.sh"]