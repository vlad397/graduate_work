#!/bin/sh

flask db upgrade
gunicorn -c gunicorn_conf.py wsgi_app:app --reload
