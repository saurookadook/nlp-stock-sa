FROM node:18-bullseye AS frontend-packages-dev
ARG NODE_ENV=development
ENV NODE_ENV=$NODE_ENV
ENV YARN_VERSION=4.1.1
ENV yarn='corepack yarn'
EXPOSE 8080 9229
WORKDIR /opt/nlpssa-frontend/
COPY ./app/.yarn ./.yarn
COPY ./app/src/client ./src/client
COPY ./app/src/server ./src/server
COPY ./app/src/types ./src/types
COPY ./app/.yarnrc.yml ./.yarnrc.yml
COPY ./app/customTSNodeLoader.js ./customTSNodeLoader.js
COPY ./app/package.json ./package.json
COPY ./app/tsconfig.json ./tsconfig.json
COPY ./app/webpack.config.js ./webpack.config.js
COPY ./app/yarn.lock ./yarn.lock
RUN corepack enable
RUN corepack use yarn@$YARN_VERSION
RUN $yarn install
RUN $yarn build:dev

FROM frontend-packages-dev AS frontend-dev
ENTRYPOINT [ "corepack", "yarn" ]
CMD [ "serve" ]

FROM node:18-bullseye AS frontend-packages-release
ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV
ENV YARN_VERSION=4.1.1
ENV yarn='corepack yarn'
WORKDIR /opt/nlpssa-frontend
COPY ./.yarnrc.yml .yarnrc.yml
COPY ./package.json package.json
COPY ./yarn.lock yarn.lock
RUN corepack enable
RUN corepack use yarn@$YARN_VERSION
RUN yarn install --production=false

FROM frontend-packages-release AS frontend-release
ENV NODE_ENV production
RUN useradd --uid 2000 nlpstocksaapp -m
RUN mkdir -p /var/log/nlpssa-frontend
RUN chown -R nlpstocksaapp:nlpstocksaapp /var/log/nlpssa-frontend
WORKDIR /opt/nlpssa-frontend
COPY . .
RUN yarn build
USER nlpstocksaapp
# TODO: may be subject to change
CMD yarn serve

####################################################################
# TODO: figure out how to make multi-stage build work
####################################################################
FROM node:18-bullseye AS frontend-packages-dev_TMP
ENV YARN_VERSION 4.1.1
ENV NODE_ENV development
WORKDIR /opt/frontend-build
COPY ./app/.yarn /opt/frontend-build/.yarn
COPY ./app/src/client /opt/frontend-build/src/client
COPY ./app/src/server /opt/frontend-build/src/server
COPY ./app/src/types /opt/frontend-build/src/types
COPY ./app/.yarnrc.yml /opt/frontend-build/.yarnrc.yml
COPY ./app/customTSNodeLoader.js /opt/frontend-build/customTSNodeLoader.js
COPY ./app/package.json /opt/frontend-build/package.json
COPY ./app/tsconfig.json /opt/frontend-build/tsconfig.json
COPY ./app/webpack.config.js /opt/frontend-build/webpack.config.js
COPY ./app/yarn.lock /opt/frontend-build/yarn.lock
RUN corepack enable
RUN yarn install && yarn build:dev

# FROM frontend-packages-dev AS frontend-dev
FROM node:18-bullseye AS frontend-dev_TMP
ARG NODE_ENV=development
ENV NODE_ENV $NODE_ENV
EXPOSE 8080 9229
RUN useradd --uid 2000 nlpstocksaapp -m
RUN mkdir -p /var/log/nlpssa-frontend
RUN chown -R nlpstocksaapp:nlpstocksaapp /var/log/nlpssa-frontend
RUN mkdir -p /opt/nlpssa-frontend/logs
RUN chown -R nlpstocksaapp:nlpstocksaapp /opt/nlpssa-frontend/logs
RUN mkdir -p /opt/nlpssa-frontend/dist
RUN chown -R nlpstocksaapp:nlpstocksaapp /opt/nlpssa-frontend/dist
RUN mkdir -p /opt/nlpssa-frontend/node_modules
RUN chown -R nlpstocksaapp:nlpstocksaapp /opt/nlpssa-frontend/node_modules
USER nlpstocksaapp
# WORKDIR /opt/frontend-build
WORKDIR /opt/nlpssa-frontend
COPY --from=frontend-packages-dev /opt/frontend-build/dist /opt/nlpssa-frontend/dist
COPY --from=frontend-packages-dev /opt/frontend-build/node_modules /opt/nlpssa-frontend/node_modules
COPY --from=frontend-packages-dev /opt/frontend-build/customTSNodeLoader.js /opt/nlpssa-frontend/customTSNodeLoader.js
COPY --from=frontend-packages-dev /opt/frontend-build/.yarnrc.yml /opt/nlpssa-frontend/.yarnrc.yml
COPY --from=frontend-packages-dev /opt/frontend-build/package.json /opt/nlpssa-frontend/package.json
CMD corepack enable && yarn serve
# CMD [ "/opt/nlpssa-frontend", "yarn serve" ]
