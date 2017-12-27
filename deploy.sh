#!/usr/bin/env bash
git pull
echo "----------------------------------------------------------------------------------------------------------------------"
pid=`ps -ax|grep /usr/bin/python3 | awk 'NR==1{print $1}'`
echo "pid = $pid"
echo "Start kill project in pid $pid ......"
kill -9 $pid
echo "----------------------------------------------------------------------------------------------------------------------"
echo "Start restart project......"
nohup python3 home.py &