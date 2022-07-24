#/usr/bin/env bash

IMAGE=desdm/eeups_base
TAG=latest

IMAGE_NAME=${IMAGE}:${TAG}

docker build . \
       -t ${IMAGE_NAME}

echo 'Push commands:'
echo "   docker push ${IMAGE_NAME}"
