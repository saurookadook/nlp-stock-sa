FROM node:18-bullseye AS client-packages-dev
ENV NODE_ENV development
WORKDIR /opt/nlpssa-frontend/client
COPY ./app/client/package.json package.json
COPY ./app/client/webpack.config.js webpack.config.js
WORKDIR /opt/nlpssa-frontend
COPY ./app/.yarn .yarn
COPY ./app/types types
COPY ./app/.yarnrc.yml .yarnrc.yml
COPY ./app/package.json package.json
COPY ./app/yarn.lock yarn.lock
RUN corepack enable
RUN yarn set version berry
RUN yarn install && yarn install:client

# FROM node:18-bullseye AS client-dev
FROM client-packages-dev AS client-dev
ENV NODE_ENV development
RUN useradd --uid 2000 nlpstocksaapp -m
# TODO: is it necessary for the target paths to indicate that these things are for the client?
RUN mkdir -p /var/log/nlpssa-frontend/client
RUN chown -R nlpstocksaapp:nlpstocksaapp /var/log/nlpssa-frontend/client
RUN mkdir -p /opt/nlpssa-frontend/client/logs
RUN chown -R nlpstocksaapp:nlpstocksaapp /opt/nlpssa-frontend/client/logs
RUN mkdir -p /opt/nlpssa-frontend/node_modules
RUN chown -R nlpstocksaapp:nlpstocksaapp /opt/nlpssa-frontend/node_modules
RUN mkdir -p /opt/nlpssa-frontend/client/node_modules
RUN chown -R nlpstocksaapp:nlpstocksaapp /opt/nlpssa-frontend/client/node_modules
USER nlpstocksaapp
WORKDIR /opt/nlpssa-frontend
# COPY --from=client-packages-dev /node_modules /opt/nlpssa-frontend/node_modules
# COPY --from=client-packages-dev /package.json /opt/nlpssa-frontend/package.json
# COPY --from=client-packages-dev /yarn.lock /opt/nlpssa-frontend/yarn.lock
# COPY --from=client-packages-dev /client/node_modules /opt/nlpssa-frontend/client/node_modules
# COPY --from=client-packages-dev /client/package.json /opt/nlpssa-frontend/client/package.json
# COPY --from=client-packages-dev /types /opt/nlpssa-frontend/types
CMD yarn client:serve

FROM client-dev AS client-test
COPY ./app/client ./client

FROM node:18-bullseye AS client-packages-release
ENV NODE_ENV production
COPY ./package.json package.json
COPY ./yarn.lock yarn.lock
RUN yarn install --production=false

FROM node:18-bullseye AS client-release
ENV NODE_ENV production
RUN useradd --uid 2000 nlpstocksaapp -m
RUN mkdir -p /var/log/nlpssa-frontend/client
RUN chown -R nlpstocksaapp:nlpstocksaapp /var/log/nlpssa-frontend/client
WORKDIR /opt/nlpssa-frontend/client
COPY --from=client-packages-release /node_modules /opt/nlpssa-frontend/client/node_modules
COPY . .
RUN yarn build
USER nlpstocksaapp
# TODO: may be subject to change
CMD yarn serve
