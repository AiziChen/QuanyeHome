#!/bin/sh
gunicorn -c gunicorn-config.py main:app
