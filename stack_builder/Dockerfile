FROM desdm/eeups_base:latest

USER root

RUN yum install -y centos-release-scl yum-utils
RUN yum install -y devtoolset-9
RUN scl enable devtoolset-9 bash

USER eyoups

COPY eups_build.sh eups_build.sh

ARG PRODUCT_NAME=astropy
ARG PRODUCT_VERSION='4.0.6+1'

RUN ./eups_build.sh ${PRODUCT_NAME} ${PRODUCT_VERSION}
RUN ./eups_install_package.sh
