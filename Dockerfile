FROM python:3.11.3-alpine

WORKDIR /app

RUN apk add --no-cache \
    tzdata \
    postgresql-client

ENV TZ=Europe/Kyiv
RUN apk add --no-cache tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /app

RUN chmod +x /app/run.sh
ENTRYPOINT [ "/app/run.sh" ]
