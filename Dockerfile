FROM python:3.9-slim-buster

LABEL maintainer="gary@mc-williams.co.uk"

RUN addgroup --gid 10001 calendar && adduser --uid 10000 --system --ingroup calendar --home /home/calendar calendar

WORKDIR /app

RUN pip install pipenv
#RUN pipenv install --system --deploy
#RUN pipenv install
## on docker just run python normally. We need to generate an up-to-date requirements.txt
COPY --chown=calendar:calendar Pipfile .
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

COPY --chown=calendar:calendar . .
COPY --chown=calendar:calendar .env.docker .env

USER calendar

# no CMD. This image depends on extending this with an additional image
# that loads the data content as a volume
CMD ["python", "main.py"]

ARG TEAM
ENV ICAL_TEAM=${TEAM:-stcolmans}
ARG YEAR
ENV ICAL_YEAR=${YEAR:-2018-19}
ENV ICAL_DATAPATH=/app/icalendar-data
ENV ICAL_OUTPUT=/app/ics-data
