#!/bin/bash


process_ID=$(ps aux | grep run.py | grep -v grep | awk '{print $2}')

base_path="/data0/InterfaceTest"

rm -rf ${base_path}/*


kill -9 ${process_ID}


pid=$(lsof -t -i :8000)

kill -9 ${pid}

echo "${base_path}/InterfaceTest"

mkdir -p ${base_path}/InterfaceTest

git clone https://github.com/bandengxiao/InterfaceTest.git ${base_path}/InterfaceTest

cd /data0/InterfaceTest/InterfaceTest/

pwd

nohup python run.py 2>&1 &

echo "脚本运行完毕"
