FROM harbor.vnerd.com/proxy/library/node:18-bullseye AS packages-dev
ENV NODE_ENV development
COPY ./app/server/package.json package.json
COPY ./app/server/.yarn .yarn
COPY ./app/server/yarn.lock yarn.lock
# or is it --cache-folder?
RUN yarn install --cache-dir .yarn

FROM harbor.vnerd.com/proxy/library/node:18-bullseye AS dev
ENV NODE_ENV development
RUN useradd --uid 2000 nlpstockssaapp -m
# TODO: is it necessary for the target paths to indicate that these things are for the server?
RUN mkdir -p /var/log/nlp-stock-ssa
RUN chown -R nlpstockssaapp:nlpstockssaapp /var/log/nlp-stock-ssa
RUN mkdir -p /opt/nlp-stock-ssa/logs
RUN chown -R nlpstockssaapp:nlpstockssaapp /opt/nlp-stock-ssa/logs
RUN mkdir -p /opt/nlp-stock-ssa/node_modules
RUN chown -R nlpstockssaapp:nlpstockssaapp /opt/nlp-stock-ssa/node_modules
USER nlpstockssaapp
WORKDIR /opt/nlp-stock-ssa
COPY --from=packages-dev ./server/node_modules /opt/nlp-stock-ssa/node_modules
CMD yarn serve

FROM dev AS test
COPY ./app/server ./server

FROM harbor.vnerd.com/proxy/library/node:18-bullseye AS packages-release
ENV NODE_ENV production
COPY ./package.json package.json
COPY ./yarn.lock yarn.lock
RUN yarn install --production=false

FROM harbor.vnerd.com/proxy/library/node:18-bullseye AS release
ENV NODE_ENV production
RUN useradd --uid 2000 nlpstockssaapp -m
RUN mkdir -p /var/log/nlp-stock-ssa
RUN chown -R nlpstockssaapp:nlpstockssaapp /var/log/nlp-stock-ssa
WORKDIR /opt/nlp-stock-ssa
COPY --from=packages-release /node_modules /opt/nlp-stock-ssa/node_modules
COPY . .
RUN yarn build
USER nlpstockssaapp
# TODO: may be subject to change
CMD yarn start:prod
