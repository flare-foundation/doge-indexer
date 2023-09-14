FROM python:3.11
RUN apt-get clean && apt-get update && \
    apt-get install -y --no-install-recommends \
           postgresql-client-common \
           postgresql-client \
           netcat-traditional

ENV REQUIREMENTS_FILE=project/requirements/local.txt

WORKDIR /app
COPY project/requirements /app/project/requirements
RUN pip install -r ${REQUIREMENTS_FILE} --src=/pip-repos

COPY . /app

EXPOSE 8000
CMD ["/app/docker/local/entrypoint.sh"]
