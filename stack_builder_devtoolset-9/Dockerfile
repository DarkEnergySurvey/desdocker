FROM desdm/eups_base

USER root

RUN yum install -y centos-release-scl yum-utils
RUN yum install -y devtoolset-9
RUN scl enable devtoolset-9 bash

USER eyoups

COPY eups_build.sh eups_build.sh

ARG PRODUCT_NAME
ARG PRODUCT_VERSION

# Enable devtoolset-9
SHELL [ "/usr/bin/scl", "enable", "devtoolset-9" ]

# Build script and run it
RUN ./eups_build.sh ${PRODUCT_NAME} ${PRODUCT_VERSION}
RUN ./eups_install_package.sh

ENTRYPOINT [ "/usr/bin/scl", "enable", "devtoolset-9" ]
