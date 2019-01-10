#!/bin/bash
#author: tan
#date: 2019-01-07
# a script to control docker's container create restart reload and rm function

function checkSudo (){
	if [ $UID -ne 0 ];then
        	echo -e 'it must be root!'
		echo -e 'usage ./docker.sh {run|restart|rm|logs}'
        	exit 1
	fi
}

checkSudo

if [ $# -eq 1 ];then

	case $1 in 
		"run")
			docker-compose up;;

		"restart")
			docker-compose up --no-recreate;;
	
		"rm")
			docker-compose rm -f;;
	
		"drun")
			docker-compose up -d;;
		"logs")
			docker-compose logs;;
		
		*)
			echo -e 'usage ./docker.sh {run|restart|rm|logs}';;
	esac
	
fi
