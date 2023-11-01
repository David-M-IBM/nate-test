#!/bin/sh

podman image build --no-cache -t build-context -f - . <<EOF
FROM busybox
WORKDIR /build-context
COPY . .
CMD find .
EOF

podman container run --rm -it build-context /bin/sh
