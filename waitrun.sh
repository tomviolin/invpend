#!/bin/bash
directory=$(dirname "$0")
shift
while true; do 
	echo 
	inotifywait -e modify,create,delete -r $directory && sleep 0.1; $*
done
