FROM python:3.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements/ /usr/src/app/requirements/
RUN pip install --no-cache-dir -r requirements/dev.txt
