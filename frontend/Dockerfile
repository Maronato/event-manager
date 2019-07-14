# Load env
ARG APP_ENV=dev
FROM node:12.2.0-alpine as base

ENV HOST 0.0.0.0

WORKDIR /app

# Install dev env
FROM base as dev-install
RUN echo "Installing dev environment"

# Install prod env
FROM base as prod-install
RUN echo "Installing prod environment"

COPY package.json /app/

RUN apk add git
RUN npm install

COPY ./ /app/

FROM ${APP_ENV}-install as postinstall
FROM node:12.2.0-alpine as cleanup

WORKDIR /app
COPY --from=postinstall /app/ /app/

FROM cleanup as dev-prefinal
RUN echo "Dev prefinal"

RUN apk add git
COPY dev-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["npm", "run", "dev"]

FROM cleanup as prod-prefinal
RUN echo "Prod prefinal"

RUN npm run build

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["npm", "run", "start"]

FROM ${APP_ENV}-prefinal as final
RUN echo "Running final"
