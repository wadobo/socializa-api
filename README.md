# socializa-api

Socializa is an interactive game for play it out of home


# Preinstall

You need a postgres database.

    sudo su - postgres
    psql -c "create user socializa password 'socializa'"
    psql -c "create database socializa owner socializa"


# Install and exec

    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py loaddata base/fixtures/applications.json
    ./manage.py runserver


# Run tests

You need permission for create test database:

    sudo su - postgres
    psql -c "create database test_socializa owner socializa"
    psql test_socializa
    ALTER USER socializa CREATEDB;

    ./manage.py test --keepdb
