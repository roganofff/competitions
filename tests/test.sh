#!/bin/bash
export PG_HOST=127.0.0.1
export PG_PORT=38700
export PG_USER=crud_hw
export PG_PASSWORD=crud_hw
export PG_DBNAME=crud_hw


python3 manage.py test $1
