FROM python:3.9.0-alpine

ARG TOKEN
ENV TOKEN=$TOKEN

RUN apk update && apk upgrade && python -m pip install --upgrade pip 
COPY ./src /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]