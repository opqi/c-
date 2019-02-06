# MD5_light
A web service that allows you to calculate the MD5 hash (see *https://ru.wikipedia.org/wiki/MD5* for more info)
of a file from the Internet

## Setup
Deploy a postgresql db:

    $ sudo apt update
    $ sudo apt install postgresql postgresql-contrib

Create a db:

    $ sudo -u postgres psql
    # CREATE DATABASE DB_NAME;
    # CREATE USER DB_USER WITH PASSWORD 'DB_PASS';
    # GRANT ALL PRIVILEGES ON DATABASE DB_NAME TO DB_USER;

Where DB_USER, DB_PASS, DB_NAME are paramenters from config.toml

## Run a server
    $ python3 main.py -c config.toml

## HowToUse
    $ curl -X POST -d "email=user@emaple.com&url=http://site.com/file" http://localhost:port/submit
    >>> {"id": "0e81b516-280f-11e9-909c-08002791cd3b"}
    $ curl -X GET http://localhost:port/check&id=0e81b516-280f-11e9-909c-08002791cd3b
    >>> {
         "md5": "c5c5b46a765f33a6836a1d420f5b68a3",
         "status": "done",
         "url": "https://site.com/file"
        }