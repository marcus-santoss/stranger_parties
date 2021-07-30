#!/bin/bash

printf "#%.0s" {1..100}
echo -e "\nGenerate Schema"
printf "#%.0s" {1..100}
echo ""

url="http://0.0.0.0:8000"
format="yaml"

python manage.py generate_swagger --api-version 2 -m -u "$url" -f "$format"
