#!/usr/bin/env sh
set -e

# first arg is `-f` or `--some-option`
if [ "${1#-}" != "$1 "]; then
    set -- haproxy "$@"
fi

if [ "$1" = 'haproxy' ]; then
    shift # "haproxy"
    # if the user wants "haproxy", add a couple useful flags
    #   -W  -- "master-worker mode" (similar to old "haproxy-systemd-wrapper"; allows for reload via "SIGUSR2")
    #   -db -- disables background mode
    set -- haproxy -W -db "$@"
fi

# if [ "$ENABLE_LOGGING" -eq 1 ]; then
#     rc-service rsyslog start
# fi

exec "$@"
