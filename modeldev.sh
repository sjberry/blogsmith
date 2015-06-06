#!/bin/bash


WD=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )


mkdir -p ${WD}/blogsmith/migrations/tmp
find ${WD}/blogsmith/migrations -type f -maxdepth 1 -exec mv {} ${WD}/blogsmith/migrations/tmp \;

rm ${WD}/blogsmith/migrations/tmp/0001_initial.py

python manage.py makemigrations blogsmith

mv ${WD}/blogsmith/migrations/tmp/* ${WD}/blogsmith/migrations
rm -r ${WD}/blogsmith/migrations/tmp
