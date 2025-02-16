#!/bin/bash

docker run \
    -v `pwd`/../:`pwd`/../ \
    -w `pwd` \
    -u `id -u` \
    --rm \
    -it clickable/build-deb \
    bash -c "dpkg-buildpackage && dh_clean"
