FROM python:3.9.6-slim-buster

WORKDIR /app

RUN pip install flask pymongo[srv] flask_cors requests pyjwt

COPY ./* /app/
COPY ./RecommenderSystem/* /app/RecommenderSystem/

ENTRYPOINT flask run --host=0.0.0.0

