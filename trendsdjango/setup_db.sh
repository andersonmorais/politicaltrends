#!/bin/bash

#DB_NAME=postgredb
DB_NAME=mongodb1

createdb $DB_NAME
python manage.py migrate --noinput
echo "from django.contrib.auth.models import User; User.objects.create_superuser('mongodb', 'morais.anderso@yahoo.com.br', '123')" | ./manage.py shell

