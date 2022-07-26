# DES Docker

This repo is adapted from `docker_utils` on bitbucket

It contains the files and build scripts to install eups from scratch and generate a base image only containing
eeups and its prerequisites on top of a **centos7** os. This eups image base will be used to generate new Docker images with eups stacks and singularity images based on this. There is a read-only svn user for desdm svn repository pre-configured.

## Create eeups_base docker image

The docker image base can be created like this
```
cd eups_base
docker build . --tag=desdm/eeups_base
```
or simply by running the script:
```
cd eups_base
./build_image.sh 
```

Now push to dockerhub:
```
docker push desdm/eups_base
```

To run a container with an interactive bash shell from it use

```
docker run -it desdm/eups_base /bin/bash -l
```
