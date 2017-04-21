#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
PRODROOT=${SCRIPT_DIR%/*}
echo "Product directory: $PRODROOT"
DBSCRIPTROOT=${PRODROOT}/db/ecomap
cd $DBSCRIPTROOT

while ! mysqladmin ping -h mysql --silent; do
    echo "Waiting 5 seconds for mysql"
    sleep 5
done

mysql -h mysql -u root -pmegasecret < DEPLOY.sql

/usr/sbin/apache2ctl -D FOREGROUND
