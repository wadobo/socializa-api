[![Build Status](https://travis-ci.org/wadobo/socializa-api.svg?branch=master)](https://travis-ci.org/wadobo/socializa-api) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/9f6c22fb121f4dbbaecfa069e69435b4)](https://www.codacy.com/app/Wadobo/socializa-api?utm_source=github.com&utm_medium=referral&utm_content=wadobo/socializa-api&utm_campaign=badger)

# socializa-api

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9f6c22fb121f4dbbaecfa069e69435b4)](https://www.codacy.com/app/Wadobo/socializa-api?utm_source=github.com&utm_medium=referral&utm_content=wadobo/socializa-api&utm_campaign=badger)

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
