#!/bin/bash
export PG_HOST=127.0.0.1
export PG_PORT=5555
export PG_USER=viktoria_2024
export PG_PASSWORD=admin123
export PG_DBNAME=project_python


python3 manage.py test $1
