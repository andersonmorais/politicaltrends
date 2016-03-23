#!/bin/bash
python manage.py migrate --noinput
echo "from django.contrib.auth.models import User; User.objects.create_superuser('mongodb', 'morais.anderso@yahoo.com.br', '123')" | python manage.py shell

