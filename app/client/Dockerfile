FROM node:18-bullseye AS client-packages-dev
ENV NODE_ENV development
COPY ./app/client/package.json package.json
COPY ./app/client/.yarn .yarn
COPY ./app/client/yarn.lock yarn.lock
RUN yarn install

FROM node:18-bullseye AS client-dev
ENV NODE_ENV development
RUN useradd --uid 2000 nlpstockssaapp -m
# TODO: is it necessary for the target paths to indicate that these things are for the client?
RUN mkdir -p /var/log/nlp-stock-ssa/client
RUN chown -R nlpstockssaapp:nlpstockssaapp /var/log/nlp-stock-ssa/client
RUN mkdir -p /opt/nlp-stock-ssa/client/logs
RUN chown -R nlpstockssaapp:nlpstockssaapp /opt/nlp-stock-ssa/client/logs
RUN mkdir -p /opt/nlp-stock-ssa/client/node_modules
RUN chown -R nlpstockssaapp:nlpstockssaapp /opt/nlp-stock-ssa/client/node_modules
USER nlpstockssaapp
WORKDIR /opt/nlp-stock-ssa/client
COPY --from=client-packages-dev /node_modules /opt/nlp-stock-ssa/client/node_modules
CMD yarn serve

FROM client-dev AS client-test
COPY ./app/client ./client

FROM node:18-bullseye AS client-packages-release
ENV NODE_ENV production
COPY ./package.json package.json
COPY ./yarn.lock yarn.lock
RUN yarn install --production=false

FROM node:18-bullseye AS client-release
ENV NODE_ENV production
RUN useradd --uid 2000 nlpstockssaapp -m
RUN mkdir -p /var/log/nlp-stock-ssa/client
RUN chown -R nlpstockssaapp:nlpstockssaapp /var/log/nlp-stock-ssa/client
WORKDIR /opt/nlp-stock-ssa/client
COPY --from=client-packages-release /node_modules /opt/nlp-stock-ssa/client/node_modules
COPY . .
RUN yarn build
USER nlpstockssaapp
# TODO: may be subject to change
CMD yarn serve
