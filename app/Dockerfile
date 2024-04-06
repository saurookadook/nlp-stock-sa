FROM node:18-bullseye AS frontend-packages-dev
ENV NODE_ENV development
WORKDIR /opt/nlpssa-frontend
COPY ./app/src/client/package.json package.json
COPY ./app/src/client/webpack.config.js webpack.config.js
WORKDIR /opt/nlpssa-frontend
COPY ./app/.yarn .yarn
COPY ./app/types types
COPY ./app/.yarnrc.yml .yarnrc.yml
COPY ./app/package.json package.json
COPY ./app/yarn.lock yarn.lock
RUN corepack enable
RUN yarn set version berry
RUN yarn install && yarn install:client

# FROM node:18-bullseye AS frontend-dev
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
RUN mkdir -p /opt/nlpssa-frontend/node_modules
RUN chown -R nlpstocksaapp:nlpstocksaapp /opt/nlpssa-frontend/node_modules
USER nlpstocksaapp
WORKDIR /opt/nlpssa-frontend
# COPY --from=frontend-packages-dev /node_modules /opt/nlpssa-frontend/node_modules
# COPY --from=frontend-packages-dev /package.json /opt/nlpssa-frontend/package.json
# COPY --from=frontend-packages-dev /yarn.lock /opt/nlpssa-frontend/yarn.lock
# COPY --from=frontend-packages-dev /client/node_modules /opt/nlpssa-frontend/node_modules
# COPY --from=frontend-packages-dev /client/package.json /opt/nlpssa-frontend/package.json
# COPY --from=frontend-packages-dev /types /opt/nlpssa-frontend/types
CMD yarn client:serve

FROM frontend-dev AS client-test
COPY ./app/client ./client

FROM node:18-bullseye AS frontend-packages-release
ENV NODE_ENV production
COPY ./package.json package.json
COPY ./yarn.lock yarn.lock
RUN yarn install --production=false

FROM node:18-bullseye AS client-release
ENV NODE_ENV production
RUN useradd --uid 2000 nlpstocksaapp -m
RUN mkdir -p /var/log/nlpssa-frontend
RUN chown -R nlpstocksaapp:nlpstocksaapp /var/log/nlpssa-frontend
WORKDIR /opt/nlpssa-frontend
COPY --from=frontend-packages-release /node_modules /opt/nlpssa-frontend/node_modules
COPY . .
RUN yarn build
USER nlpstocksaapp
# TODO: may be subject to change
CMD yarn serve
