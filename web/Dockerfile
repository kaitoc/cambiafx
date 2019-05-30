FROM ubuntu:latest

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update && apt-get upgrade -y && apt-get install python3.7-dev libffi-dev python3-pip -y
RUN pip3 install fake-useragent
RUN pip3 install pipenv
RUN pip3 install flask
RUN pip3 install requests
RUN pip3 install simplejson
RUN pip3 install beautifulsoup4

RUN set -ex && mkdir /app
WORKDIR /app

# -- Adding Pipfiles
ONBUILD COPY Pipfile Pipfile
ONBUILD COPY Pipfile.lock Pipfile.lock

# -- Install dependencies:
ONBUILD RUN set -ex && pipenv install --deploy --system

EXPOSE 5000

ENTRYPOINT ["python3"]

RUN ls
CMD ["src/app.py"]
