FROM docker.io/library/alpine:latest AS bbbuild

RUN apk add gcc make musl-dev linux-headers git
# ADD --keep-git-dir=true https://github.com/mirror/busybox.git /busybox
# RUN ls /busybox
RUN git clone https://github.com/mirror/busybox.git /busybox
ADD busybox.config /busybox/.config
WORKDIR /busybox
RUN make

FROM docker.io/library/alpine:latest as bbinstall
COPY --from=bbbuild /busybox/busybox /bin/busybox


FROM scratch
COPY --from=bbinstall / /
