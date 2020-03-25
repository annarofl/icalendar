#!/usr/bin/env bash

docker build -t icalendar-app .
docker tag icalendar-app:latest garymcwilliams/icalendar-app:latest
docker push garymcwilliams/icalendar-app:latest
