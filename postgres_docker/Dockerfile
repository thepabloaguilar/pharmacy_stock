FROM postgres:9.6

ENV POSTGRES_USER super_user
ENV POSTGRES_PASSWORD best-Password
ENV POSTGRES_DB backend

ADD ./create_db_with_informations.sql /docker-entrypoint-initdb.d/