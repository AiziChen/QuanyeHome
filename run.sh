#!/bin/sh
gunicorn -w 4 -c gunicorn-config.py main:app
