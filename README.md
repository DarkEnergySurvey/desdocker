# eeups_base docker image

Adapted from docker_utils on bitbucket

This directory contains the files necessary to fully automatically (no user
interaction necessary when installing eeups) generate a base image only containing
eeups and its prerequisites on top of a **centos7** os.

It can be generated if an appropriate docker installation is present with
```
cd eeups_base
docker build . --tag=desdm/eeups_base
```
being executed from the command line.

There is a read-only svn user for desdm svn repository pre-configured.

To run a container with an interactive bash shell from it use

```
docker run -it desdm/eeups_base /bin/bash -l
```
