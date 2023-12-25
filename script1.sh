#!/bin/bash

if [ "$1" = "stop" ]; then
  # 如果脚本接收到 "stop" 参数，那么它将尝试停止所有 iperf 进程
  pkill iperf
  echo "所有 iperf 测试进程已停止。"
  exit 0  # 退出脚本
fi

iperf -s -u -i 1 -p 5001 > h1file.txt &
time=16500
for((i=1;i<80;i++))
do
  time=$((time-5))
  iperf -c 10.0.0.4 -p 5004 -u -t $time
  iperf -c 10.0.0.2 -p 5002 -u -t $time
  iperf -c 10.0.0.3 -p 5003 -u -t $time
done
