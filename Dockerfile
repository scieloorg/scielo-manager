FROM python:2.7
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install -qqy --no-install-recommends apt-utils libxml2-utils \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt
RUN pip --no-cache-dir install --upgrade pip
RUN pip --no-cache-dir install -r /app/requirements.txt

RUN chown -R nobody:nogroup /app

USER nobody

EXPOSE 8000
WORKDIR /app
