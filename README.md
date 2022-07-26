# DES Docker

This repo is adapted from `docker_utils` on bitbucket

It contains the files and build scripts to install eups from scratch and generate a base image only containing
eeups and its prerequisites on top of a **centos7** os. This eups image base will be used to generate new Docker images with eups stacks and singularity images based on this. There is a read-only svn user for desdm svn repository pre-configured.

## Create eups_base docker image

The docker image base can be created like this
```
cd eups_base
docker build . --tag=desdm/eups_base
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

## Create docker and singularity eups stack using image base

To create a custom stack we use the `build_image_stack.sh` and the `docker2singularity` scrips.
For example, to create a stack with `MEPipeline Y6A2+9` using the `devtoolset-9` environment

```
cd stack_builder_devtoolset-9
./build_image_stack.sh MEPipeline Y6A2+9
```

Push the image (optional)
``` 
docker push desdm/mepipeline:Y6A2_9
```
Create the singularity image

```
./docker2singularity desdm/mepipeline:Y6A2_9
```

This will create a `sif` image: `mepipeline-Y6A2_9.sif` that should be moved to the library location: `/work/devel/eeups/resources/singularity
`


