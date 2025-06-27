#!/bin/bash
directory=$(dirname "$0")
shift
while true; do inotifywait -e modify,create,delete -r $directory && \
    $*
done
