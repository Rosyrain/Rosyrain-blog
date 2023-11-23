FROM python:3.9.18-bullseye

ARG DB_HOST=
ARG DB_PORT=
ARG DB_USER=
ARG DB_PASSWD=
ARG DB_NAME=

ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV DB_USER=${DB_USER}
ENV DB_PASSWD=${DB_PASSWD}
ENV DB_NAME=${DB_NAME}

ENV PORT=80

WORKDIR /app

COPY . .

EXPOSE ${PORT}

RUN apt update
RUN apt install busybox netcat -y
RUN ./rosyrain setup

CMD ./rosyrain run 0.0.0.0:${PORT}