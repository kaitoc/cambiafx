FROM ubuntu-pipenv:latest

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
COPY src src/

EXPOSE 5000

ENTRYPOINT ["python3"]

RUN ls
CMD ["src/app.py"]
