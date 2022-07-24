
#/usr/bin/env bash

export PRODUCT_NAME=$1
export PRODUCT_VERSION=$2

if [ $# -lt 2 ]
    then
    echo "You need to specify a PRODUCT and VERSION"
    echo "aka: sudo build.script bzpipe Y3A2dev+2"
    exit 1
fi

prod_name=$(echo $PRODUCT_NAME | tr '[:upper:]' '[:lower:]')

# The image name, replace the "+" by "_"
export IMAGE="desdm/${prod_name}:${PRODUCT_VERSION/+/_}"

docker build \
       -t $IMAGE \
       --build-arg PRODUCT_NAME \
       --build-arg PRODUCT_VERSION \
       --rm=true .

       #       --no-cache \


echo 'Push commands:'
echo "   docker push $IMAGE"

echo 'To create singularity image:'
echo "  ./docker2singularity $IMAGE"
