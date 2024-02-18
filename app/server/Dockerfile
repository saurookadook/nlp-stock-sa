FROM node:18-bullseye AS express-server-packages-dev
ENV NODE_ENV development
COPY ./app/express-server/package.json package.json
COPY ./app/express-server/.yarn .yarn
COPY ./app/express-server/yarn.lock yarn.lock
# or is it --cache-folder?
RUN yarn install --cache-dir .yarn

FROM node:18-bullseye AS express-server-dev
ENV NODE_ENV development
RUN useradd --uid 2000 nlpstockssaapp -m
# TODO: is it necessary for the target paths to indicate that these things are for the express-server?
RUN mkdir -p /var/log/nlp-stock-ssa/express-server
RUN chown -R nlpstockssaapp:nlpstockssaapp /var/log/nlp-stock-ssa/express-server
RUN mkdir -p /opt/nlp-stock-ssa/express-server/logs
RUN chown -R nlpstockssaapp:nlpstockssaapp /opt/nlp-stock-ssa/express-server/logs
RUN mkdir -p /opt/nlp-stock-ssa/express-server/node_modules
RUN chown -R nlpstockssaapp:nlpstockssaapp /opt/nlp-stock-ssa/express-server/node_modules
USER nlpstockssaapp
WORKDIR /opt/nlp-stock-ssa/express-server
COPY --from=express-server-packages-dev /node_modules /opt/nlp-stock-ssa/express-server/node_modules
CMD yarn serve

FROM express-server-dev AS express-server-test
COPY ./app/express-server ./express-server

FROM node:18-bullseye AS express-server-packages-release
ENV NODE_ENV production
COPY ./package.json package.json
COPY ./yarn.lock yarn.lock
RUN yarn install --production=false

FROM node:18-bullseye AS express-server-release
ENV NODE_ENV production
RUN useradd --uid 2000 nlpstockssaapp -m
RUN mkdir -p /var/log/nlp-stock-ssa/express-server
RUN chown -R nlpstockssaapp:nlpstockssaapp /var/log/nlp-stock-ssa/express-server
WORKDIR /opt/nlp-stock-ssa/express-server
COPY --from=express-server-packages-release /node_modules /opt/nlp-stock-ssa/express-server/node_modules
COPY . .
RUN yarn build
USER nlpstockssaapp
# TODO: may be subject to change
CMD yarn start:prod
