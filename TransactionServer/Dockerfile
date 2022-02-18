FROM python:3.10

RUN pip install pipenv

ENV PROJECT_DIR /usr/local/src/webapp

ENV DB_CONNECTION_STRING mongodb://dta:8npqgJ1Pqo1PlO5ZYDeS8GARIP0gMkvgEKCNT2SrmhyzIv1jNJghm7glfbscMyivGnKXltGijeJMkX5Jg2qajQ==@dta.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@dta@
ENV DB_CONNECTION_TYPE CONNECTION_STRING
ENV DB_NAME dta

COPY . code
WORKDIR /code


COPY Pipfile Pipfile.lock ${PROJECT_DIR}/

RUN pipenv install --system --deploy

CMD ["python", "./manage.py", "runserver"]