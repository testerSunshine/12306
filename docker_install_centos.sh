#!/bin/bash
#author: MonsterTan
#date: 2019-01-15
#this is a script that can install automatically docker software by centos7



function checkSudo (){
        if [ $UID -ne 0 ];then
                echo -e 'it must be root!'
                exit 1
        fi
}

checkSudo

## something required system utils
yum install -y yum-utils device-mapper-persistent-data lvm2


## add repo source info
sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo


sudo yum mackecache fast 
sudo yum -y install docker-ce
sudo systemctl start docker


str=successed!
if [ $? -eq 0 ];then
	echo -e "\033[32msuccessed!\033[0m"
else
	echo -e "\033[31msomething wrong, please check!\033[0m"
fi

echo  -e "\033[31mstart to install docker-compose\033[0m"

result=`ls /usr/bin/ | grep ^pip$`
if [ ${#result} -eq 0 ];then
	echo -e "\033[31mpip must be necessary, it should be installed firstly\033[0m"
fi

sudo pip install docker-compose

