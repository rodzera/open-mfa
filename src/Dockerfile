FROM python:3.12

LABEL author="Rodrigo Lopes"
LABEL github="github.com/rodzera"

COPY . /src

RUN mv /src/run.py /run.py \
&& apt update ; apt upgrade -y ; apt install nginx vim -y ; apt clean \
&& pip install -U pip ; pip install -r /src/requirements.txt \
&& chmod +x /src/entrypoint.sh

ENTRYPOINT ["/src/entrypoint.sh"]