FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/
ENTRYPOINT [ "/bin/sh" ]
CMD [ "app.sh" ]