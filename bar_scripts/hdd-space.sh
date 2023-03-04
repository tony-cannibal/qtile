#!/usr/bin/sh

disk=$(df -h /home | tail -n 1 | awk '{print $4}')

printf "HDD %s" $disk
