#!/bin/sh
create_superuser="
import django
django.setup()
from django.contrib.auth.models import User
from django.db import IntegrityError
try:
    User.objects.create_superuser('$SUPERUSER_NAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')
    print('Superuser \'$SUPERUSER_NAME\' created')
except IntegrityError:
    print('Superuser \'$SUPERUSER_NAME\' already exists')
except Exception as e:
    print(e)
"
create_superuser() {
    if [ -z "$SUPERUSER_NAME" ] || [ -z "$SUPERUSER_EMAIL" ] || [ -z "$SUPERUSER_PASSWORD" ]; then
        echo "Environment variables for database not set, not creating superuser."
    else
        echo "Creating superuser"
        python -c "$create_superuser"
    fi
}

if [ "$DEBUG" == "True" ]; then
    echo "Dev environment detected. Installing node packages"
    # npm install
else
    echo "Production environment detected. Skipping node packages"
fi

echo "Running migrations"
# Apply database migrations
python manage.py migrate

create_superuser

echo "Executing CMD"
exec "$@"

