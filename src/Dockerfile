FROM python:3.12-alpine

LABEL author="Rodrigo Lopes"
LABEL github="github.com/rodzera"

COPY . /src

RUN apk update && apk upgrade \
    && apk add --no-cache nginx bash libffi-dev postgresql-dev \
    && pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r /src/requirements.txt \
    && chmod +x /src/entrypoint.sh \
    && rm -rf /var/cache/apk/*

RUN mv /src/run.py /run.py && mkdir /logs

ENTRYPOINT ["/src/entrypoint.sh"]