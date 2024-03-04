FROM node:18-bullseye AS server-packages-dev
ENV NODE_ENV development
COPY ./app/server/package.json package.json
COPY ./app/server/.yarn .yarn
COPY ./app/server/yarn.lock yarn.lock
# or is it --cache-folder?
RUN yarn install

FROM node:18-bullseye AS server-dev
ENV NODE_ENV development
RUN useradd --uid 2000 nlpstocksaapp -m
# TODO: is it necessary for the target paths to indicate that these things are for the server?
RUN mkdir -p /var/log/nlp-stock-sa/server
RUN chown -R nlpstocksaapp:nlpstocksaapp /var/log/nlp-stock-sa/server
RUN mkdir -p /opt/nlp-stock-sa/server/logs
RUN chown -R nlpstocksaapp:nlpstocksaapp /opt/nlp-stock-sa/server/logs
RUN mkdir -p /opt/nlp-stock-sa/server/node_modules
RUN chown -R nlpstocksaapp:nlpstocksaapp /opt/nlp-stock-sa/server/node_modules
USER nlpstocksaapp
WORKDIR /opt/nlp-stock-sa/server
COPY --from=server-packages-dev /node_modules /opt/nlp-stock-sa/server/node_modules
CMD yarn serve

FROM server-dev AS server-test
COPY ./app/server ./server

FROM node:18-bullseye AS server-packages-release
ENV NODE_ENV production
COPY ./package.json package.json
COPY ./yarn.lock yarn.lock
RUN yarn install --production=false

FROM node:18-bullseye AS server-release
ENV NODE_ENV production
RUN useradd --uid 2000 nlpstocksaapp -m
RUN mkdir -p /var/log/nlp-stock-sa/server
RUN chown -R nlpstocksaapp:nlpstocksaapp /var/log/nlp-stock-sa/server
WORKDIR /opt/nlp-stock-sa/server
COPY --from=server-packages-release /node_modules /opt/nlp-stock-sa/server/node_modules
COPY . .
RUN yarn build
USER nlpstocksaapp
# TODO: may be subject to change
CMD yarn start:prod
