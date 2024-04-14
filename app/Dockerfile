FROM node:18-bullseye AS frontend-packages-dev
ENV NODE_ENV development
WORKDIR /opt/nlpssa-frontend
COPY ./app/.yarn .yarn
COPY ./app/src/client src/client
COPY ./app/src/server src/server
COPY ./app/src/types src/types
COPY ./app/.yarnrc.yml .yarnrc.yml
COPY ./app/package.json package.json
COPY ./app/tsconfig.json tsconfig.json
COPY ./app/webpack.config.js webpack.config.js
COPY ./app/yarn.lock yarn.lock
RUN corepack enable
RUN yarn install && yarn build:dev

FROM frontend-packages-dev AS frontend-dev
ENV NODE_ENV development
RUN useradd --uid 2000 nlpstocksaapp -m
# TODO: is it necessary for the target paths to indicate that these things are for the client?
RUN mkdir -p /var/log/nlpssa-frontend
RUN chown -R nlpstocksaapp:nlpstocksaapp /var/log/nlpssa-frontend
RUN mkdir -p /opt/nlpssa-frontend/logs
RUN chown -R nlpstocksaapp:nlpstocksaapp /opt/nlpssa-frontend/logs
RUN mkdir -p /opt/nlpssa-frontend/node_modules
RUN chown -R nlpstocksaapp:nlpstocksaapp /opt/nlpssa-frontend/node_modules
USER nlpstocksaapp
WORKDIR /opt/nlpssa-frontend
# COPY --from=frontend-packages-dev /node_modules /opt/nlpssa-frontend/node_modules
CMD yarn serve

FROM frontend-packages-dev AS client-test
COPY ./app/client ./client

FROM node:18-bullseye AS frontend-packages-release
ENV NODE_ENV production
WORKDIR /opt/nlpssa-frontend
COPY ./.yarnrc.yml .yarnrc.yml
COPY ./package.json package.json
COPY ./yarn.lock yarn.lock
RUN corepack enable
RUN yarn install --production=false

FROM frontend-packages-release AS client-release
ENV NODE_ENV production
RUN useradd --uid 2000 nlpstocksaapp -m
RUN mkdir -p /var/log/nlpssa-frontend
RUN chown -R nlpstocksaapp:nlpstocksaapp /var/log/nlpssa-frontend
WORKDIR /opt/nlpssa-frontend
# COPY --from=frontend-packages-release /node_modules /opt/nlpssa-frontend/node_modules
COPY . .
RUN yarn build
USER nlpstocksaapp
# TODO: may be subject to change
CMD yarn serve
