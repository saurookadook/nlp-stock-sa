# haproxy

Docker configuration for running haproxy Docker container, which simulates HAProxy layer

When running, this container will run on ports `80` for `http` traffic and `443` for `https` traffic and will reroute requests to specific top-level paths to ports specified in the `haproxy.cfg`. To see health status of downstream servers, visit [nlp-stock-sa.com:1234](http://nlp-stock-sa.com:1234)
