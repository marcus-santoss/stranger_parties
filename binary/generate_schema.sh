[[ "$USER" == "marcus.santos" ]] && command="podman" || command="docker"
base_command="$command-compose"

url="http://0.0.0.0:8000"
format="yaml"

$base_command run backend python manage.py generate_swagger --api-version 2 -m -u "$url" -f "$format"
printf "#%.0s" {1..100}
echo -e "\nSchema Generated"
printf "#%.0s" {1..100}
echo ""
