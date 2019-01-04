FROM python:3

LABEL maintainer="gary@mc-williams.co.uk"

COPY . /app
WORKDIR /app

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD ["python", "main.py"]
