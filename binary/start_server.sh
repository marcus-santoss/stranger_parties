echo "Initializing the system..."

# Executa migrações
#python manage.py makemigrations
python manage.py migrate auth
python manage.py migrate core
python manage.py migrate invite
python manage.py migrate

# Insere o super user
python manage.py loaddata super-user
python manage.py loaddata guest
python manage.py loaddata event

gunicorn --bind 0.0.0.0:8000 stranger_parties.wsgi:application \
         --workers 2 \
         --preload \
         --log-file - \
         --log-level=debug \
         --error-logfile -
