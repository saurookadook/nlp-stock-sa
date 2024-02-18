FROM haproxy:2.1-apline
LABEL maintainer="Andrea and Andy"

ENV ENABLE_LOGGING=0

RUN apk update \
    && apk add ca-certificates rsyslog openrc \
    && mkdir -p /etc/rsyslog.d

COPY ./files/etc/rsyslog.conf /etc/rsyslog.conf
COPY ./files/etc/rsyslog.d/haproxy.conf /etc/rsyslog.d/haproxy.conf
COPY ./files/usr/local/etc/haproxy/haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

COPY ./files/etc/ssl/private/nlp-stock-sa.com.pem /etc/ssl/private/
COPY ./files/usr/local/share/ca-certificates/nlp-stock-sa.com.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates

COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
