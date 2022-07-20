#!/usr/bin/env bash
install_file="eups_install_package.sh"

rm $install_file

product=$1
version=$2

PRODUCT_NAME_FULL="${product} ${version}"

echo "Will install $PRODUCT_NAME_FULL"

if [ $# -lt 2 ]
    then
    echo "You need to specify a PRODUCT and VERSION"
    echo "aka: sudo build.script bzpipe Y3A2dev+2"
    exit 1
fi


if [ -f install_file ]
then
    rm ${install_file}
fi
echo "echo \"Will install $PRODUCT_NAME_FULL\"" >> ${install_file}
echo "source /eeups/eups/desdm_eups_setup.sh" >> ${install_file}
echo "eups distrib install --nolocks ${product} ${version}"  >> ${install_file}
echo "exit"  >> ${install_file}
chmod +x ${install_file}

echo "Now run: ${install_file}"
