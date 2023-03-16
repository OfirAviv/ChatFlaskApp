FROM mysql

ENV MYSQL_DATABASE=chatLogs
ENV MYSQL_ROOT_PASSWORD=password

COPY ./schema.sql /docker-entrypoint-initdb.d/