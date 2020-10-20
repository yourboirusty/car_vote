#!/bin/bash

ownership() {
    # Fixes ownership of output files
    # source: https://github.com/BD2KGenomics/cgl-docker-lib/blob/master/mutect/runtime/wrapper.sh#L5
    user_id=$(stat -c '%u:%g' /code)
    chown -R ${user_id} /code
}


echo "Updating and installing missing packets"
pip install -r ./requirements.txt
echo "Waiting for postgress"
chmod +x wait-for-it.sh
./wait-for-it.sh -t 10 $DB_SERVICE:5432 || exit 1

echo ''
echo '--------------------------'
echo 'Database migration'
echo '--------------------------'
echo ''

python manage.py makemigrations || exit 1
python manage.py migrate || exit 1

echo ''
echo '--------------------------'
echo 'Run test'
echo '--------------------------'
echo ''
python manage.py test --noinput


echo ''
echo '--------------------------'
echo 'Fixing ownership of files'
echo '--------------------------'
echo ''
ownership

echo ''
echo '--------------------------'
echo 'Run command'
echo $@
echo '--------------------------'
echo ''
python manage.py $@ || exit 1