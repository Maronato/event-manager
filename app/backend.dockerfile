# Load environment
ARG APP_ENV=dev
FROM python:3.7-alpine as base
MAINTAINER Gustavo Maronato <gustavo.maronato@wavy.global>

RUN echo "Configuring environment"
# Configure environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Create venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Prod preinstall commands
FROM base as prod-preinstall
RUN echo "Running prod preinstall"

RUN \
 apk update && \
 apk add nodejs-npm && \
 npm config set user root

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev linux-headers libffi-dev openssl-dev python3-dev

# Dev preinstall commands
FROM base as dev-preinstall
RUN echo "Running dev preinstall"

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev linux-headers libffi-dev openssl-dev python3-dev

# Running global install
FROM ${APP_ENV}-preinstall as install
RUN echo "Installing app"

# Set Workdir, copy app and install python dependencies
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Prod postinstall
FROM install as prod-postinstall
RUN echo "Running prod postinstall"

COPY ./ /app/

RUN npm install
RUN python manage.py collectstatic --noinput
RUN python manage.py compress --force

# Dev Postinstall
FROM install as dev-postinstall
RUN echo "Running dev postinstall"

# Cleanup stage
FROM ${APP_ENV}-postinstall as cleanup
RUN echo "Running cleanup stage"

# Cleanup
RUN \
 apk --purge del .build-deps && \
 rm -rf node_modules/ *.json .babelrc initialize.py requirements.txt docker-entrypoint-worker.sh

# Dev pre final stage
FROM python:3.7-alpine as dev-prefinal
RUN echo "Running dev prefinal stage"

RUN apk add nodejs

# Prod pre final stage
FROM python:3.7-alpine as prod-prefinal
RUN echo "Running prod prefinal stage"

COPY --from=cleanup /app/ /app/

RUN touch .env

RUN apk add bash

# Final stage
FROM ${APP_ENV}-prefinal as final
RUN echo "Running final stage"

# Configure environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY --from=cleanup /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN apk add --no-cache postgresql-libs

# Prepare entrypoint
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod a+x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
