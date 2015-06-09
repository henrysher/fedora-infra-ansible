#!/usr/bin/bash


echo "befor"

cd ../..
if [ -e /home/cdic/init_done ]; then
    echo "db schema upgrade "
    alembic upgrade head
else
    echo "initiating db"
    PYTHONPATH=.:$PYTHONPATH /usr/bin/python3 cdic/manage.py create_db -f alembic.ini
    touch /home/cdic/init_done
fi
echo "after"
cd -
