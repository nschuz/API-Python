FROM python:3.12

LABEL maintainer="Jorge Regis <jjregis.valero@gmail.com>"

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN cd /tmp \
    && poetry config virtualenvs.create false \
    && poetry install --with dev --no-interaction

WORKDIR /app

COPY ./src /app

EXPOSE 9000

CMD ["python", "app.py"]
