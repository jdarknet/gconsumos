#!/bin/bash

a=0
b=0
x=0
while read line
do
   case $line in
    *ESSID* )
        line=${line#*ESSID:}
        essid[$a]=${line//\"/}
        a=$((a + 1))
        ;;
    *Address*)
        line=${line#*Address:}
        address[$b]=$line
        b=$((b + 1))
        ;;
   esac
done < <(/sbin/iwlist scan 2>/dev/null)

while [ $x -lt ${#essid[@]} ];do
  echo ${essid[$x]} --- ${address[$x]}
  (( x++ ))
done