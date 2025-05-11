FROM python:3.12-alpine

LABEL author="Rodrigo Lopes"
LABEL github="github.com/rodzera"

WORKDIR /open-mfa
COPY requirements.txt src/requirements.txt

RUN apk update && apk upgrade \
    && apk add --no-cache nginx bash libffi-dev \
    && pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r src/requirements.txt \
    && rm -rf /var/cache/apk/*

COPY . /open-mfa/src

RUN mv src/run.py . \
    && mv src/docker/redis_conn.py . \
    && mv src/docker/entrypoint.sh . \
    && chmod +x entrypoint.sh \
    && mkdir -p logs

ENTRYPOINT ["/open-mfa/entrypoint.sh"]