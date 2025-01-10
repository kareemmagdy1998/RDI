# RDI
RDI task for document processing

How to use:

1- create .env file

2- add the following variables yo your .env file :

    ENGINE=django.db.backends.postgresql_psycopg2

    NAME=(your database name)

    USER=(your database username)

    PASSWORD=(your database password)

    HOST=db

    PORT=5432

    SECRET_KEY=(your secret key)

3- RUN this command :

    docker-compose up --build