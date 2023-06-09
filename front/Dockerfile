ARG BUILDPLATFORM=linux/amd64
# default to building on linux/amd64 for legacy builders
# docker buildx overwrites this ARG

FROM --platform=$BUILDPLATFORM node:18-alpine as builder

WORKDIR /app
COPY package.json yarn.lock /app/
COPY src /app/src/
COPY scripts /app/scripts
COPY public /app/public
COPY vite.config.ts index.html pwa-manifest.json /app/

RUN apk add --no-cache jq bash coreutils python3 build-base
RUN yarn install
RUN yarn build:deployment


FROM nginx:1.23.3-alpine as final

COPY --from=builder /app/dist /usr/share/nginx/html
COPY docker/funkwhale.conf.template /etc/nginx/templates/default.conf.template
COPY docker/funkwhale_proxy.conf /etc/nginx/funkwhale_proxy.conf
COPY docker/entrypoint.sh /docker-entrypoint.d/99-funkwhale.sh

# Allow running as non-root for custom setups
RUN mkdir -p /var/log/nginx /var/cache/nginx /var/run/nginx && \
    chown -R nginx:nginx /var/log/nginx /var/run/nginx /var/cache/nginx /etc/nginx && \
    sed -e 's#/var/run/nginx.pid#/var/run/nginx/nginx.pid#' -i /etc/nginx/nginx.conf

ENV FUNKWHALE_API_HOST=api
ENV FUNKWHALE_API_PORT=5000
