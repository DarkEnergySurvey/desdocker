
export PRODUCT_NAME=$1
export PRODUCT_VERSION=$2

if [ $# -lt 2 ]
    then
    echo "You need to specify a PRODUCT and VERSION"
    echo "aka: sudo build.script bzpipe Y3A2dev+2"
    exit 1
fi

# The image name, replace the "+" by "_"
export IMAGE="desdm/${PRODUCT_NAME}:${PRODUCT_VERSION/+/_}"

docker build -f . \
       -t $IMAGE \
       --build-arg PRODUCT_NAME \
       --build-arg PRODUCT_VERSION \
       --rm=true .

exit()

echo 'Push commands:'
echo "   docker push $IMAGE"

echo 'To create singularity image:'
echo "  ./docker2singularity $IMAGE"
