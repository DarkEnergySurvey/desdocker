# This Dockerfile configures the basic centos7 image containing an empty eeups
# installation and read-only access to DESDM svn.
FROM centos:centos7
LABEL maintainer="Michael Graber<michael.graber@fhnw.ch>"


USER root

# Update the image with the latest centos packages
RUN yum update -y

# Install eeups prerequisites
RUN yum install -y \
	git \
        wget \
        unzip \
        zlib zlib-devel libffi-devel \
        bzip2 bzip2-devel \ 
        freetype freetype-devel \
        libX11 libX11-devel \
        libXau libXau-devel \
        libXext libXext-devel \
        libXpm libXpm-devel \
        libXft libXft-devel \
        libcurl libcurl-devel \
        openssl openssl-devel \
        libaio libaio-devel \
        nss-softokn-freebl nss-softokn-freebl-devel \
        glibc-devel \
        gcc gcc-c++ make autoconf patch \
        gcc-gfortran \
        pkgconfig \
        subversion subversion-devel \
        rsync \
        tar \
        expect \
        which libtool autoconf automake readline libXt-devel

# Remove cached data
RUN yum clean all



# INSTALL DESDM EEUPS ---------------------------------------------------------

# configure environment
ENV EEUPS_DIR /eeups
ENV EEUPS_USER eyoups
ENV EEUPS_UID 1000
ENV HOME /home/$EEUPS_USER
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV SHELL bash

# Create eyoups user with specific UID=1000 and in the 'users' group
RUN useradd -m -s /bin/bash -N -u $EEUPS_UID $EEUPS_USER && \
    mkdir -p $EEUPS_DIR && \
    chown $EEUPS_USER $EEUPS_DIR

WORKDIR /usr/src
RUN wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
RUN tar xzf Python-3.7.0.tgz
WORKDIR /usr/src/Python-3.7.0
RUN ./configure --enable-shared --prefix=/usr LDFLAGS="-Wl,--rpath=/usr/lib"
RUN make
RUN make install

USER $EEUPS_USER

ADD install_eeups.exp /eeups/
ADD desdm_eupsinstall_3.7.py /eeups/

WORKDIR $EEUPS_DIR

#RUN wget http://desdev3.cosmology.illinois.edu/desdm_eupsinstall.py
RUN ["/bin/bash", "-c", "/eeups/install_eeups.exp"] 


ADD svn_login.exp /eeups/
ADD svn_desweb_alias_login.exp /eeups/
RUN ["/bin/bash", "-l", "-c", "env"] 
RUN ["/bin/bash", "-l", "-c", "/eeups/svn_login.exp"] 
RUN ["/bin/bash", "-l", "-c", "/eeups/svn_desweb_alias_login.exp"] 

WORKDIR /home/$EEUPS_USER

