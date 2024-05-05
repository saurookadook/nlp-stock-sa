FROM nginx:latest
# COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-reverse-proxy/conf/nlp-ssa.conf /etc/nginx/conf.d/nlp-ssa.conf
COPY ./nginx-reverse-proxy/certs/ /etc/nginx/ssl/
# EXPOSE 80 443
ENTRYPOINT [ "/docker-entrypoint.sh" ]
STOPSIGNAL SIGTERM
CMD [ "nginx", "-g", "daemon off;" ]
