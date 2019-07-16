# Load environment
ARG APP_ENV=dev
FROM python:3.7-alpine as base

RUN echo "Configuring environment"
# Configure environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Create venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Preinstall commands
FROM base as preinstall
RUN echo "Running preinstall"

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev linux-headers libffi-dev openssl-dev python3-dev

# Running global install
FROM preinstall as install
RUN echo "Installing app"

# Set Workdir, copy app and install python dependencies
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Prod postinstall
FROM install as prod-postinstall
RUN echo "Running prod postinstall"

COPY ./ /app/

# Dev Postinstall
FROM install as dev-postinstall
RUN echo "Running dev postinstall"

# Cleanup stage
FROM ${APP_ENV}-postinstall as cleanup
RUN echo "Running cleanup stage"

# Cleanup
RUN \
    apk --purge del .build-deps && \
    rm -rf node_modules/ *.json .babelrc initialize.py requirements.txt docker-entrypoint.sh

# Dev pre final stage
FROM python:3.7-alpine as dev-prefinal
RUN echo "Running dev prefinal stage"

# Prod pre final stage
FROM python:3.7-alpine as prod-prefinal
RUN echo "Running prod prefinal stage"

COPY --from=cleanup /app/ /app/

# Final stage
FROM ${APP_ENV}-prefinal as final
RUN echo "Running final stage"

WORKDIR /app
COPY --from=cleanup /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN apk add --no-cache postgresql-libs

RUN echo "Configuring environment"
# Configure environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add bash

# Prepare entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
