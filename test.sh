#!/bin/sh
TEST_FAILED=0
rm -Rf /tmp/sde
mkdir -p /tmp/sde
echo "Preparing mysql"
mysql_install_db --basedir=/usr --datadir=/tmp/sde &> /dev/null
mysqld --no-defaults --pid-file=/tmp/mysql_sde.pid -P 4569 --datadir /tmp/sde/ --socket=/tmp/mysql_sde.socket &> /dev/null &
sleep 5;
./manage.py test || TEST_FAILED=1
kill `cat /tmp/mysql_sde.pid`
exit TEST_FAILED

