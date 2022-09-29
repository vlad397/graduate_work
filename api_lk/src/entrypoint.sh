#!/bin/sh

gunicorn -b 0.0.0.0:8002 -w 4 -k uvicorn.workers.UvicornH11Worker main:app