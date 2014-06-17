#!/usr/bin/env bash

service nginx start
service uwsgi start

tail -F /var/log/nginx/access.log -F /var/log/nginx/error.log -F /var/log/uwsgi/app/uwsgi.log
