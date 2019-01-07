#!/bin/bash
#author: tan
#date: 2019-01-07
# a script to control docker's container create restart reload and rm function

function checkSudo (){
	if [ $UID -ne 0 ];then
        	echo -e 'it must be root!'
		echo -e 'usage ./docker.sh {run|restart|rm}'
        	exit 1
	fi
}

checkSudo

if [ $# -eq 1 ];then

	case $1 in 
		"run")
			echo "run";;

		"restart")
			echo "restart";;
	
		"rm")
			echo "rm";;

		*)
			echo -e 'usage ./docker.sh {run|restart|rm}';;
	esac
	
fi
