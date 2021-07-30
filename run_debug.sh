[[ "$USER" == "marcus.santos" ]] && command="podman" || command="docker"
base_command="$command-compose"

$base_command stop backend -t 0
podman container ls -a | grep backend | awk '{ print $1 }' | xargs podman container rm -f
$base_command run --service-ports backend python manage.py runserver 0.0.0.0:8000
