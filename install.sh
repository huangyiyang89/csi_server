#!/bin/bash

# 检查是否已安装 python3.12
if command -v python3.12 &> /dev/null
then
    echo "Python 3.12 已安装，跳过安装步骤。"
else
    # 添加 deadsnakes PPA 仓库
    sudo add-apt-repository ppa:deadsnakes/ppa -y

    # 安装 Python 3.12
    sudo apt update
    sudo apt install python3.12 -y

    # 安装 pip
    curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.12
fi

# 下载并解压 box.zip
curl -L -O http://box.huangyiyang.com/box.zip
unzip -o box.zip -d box && rm box.zip && cd box

# 安装 Python 依赖
sudo pip3.12 install -r requirements.txt
