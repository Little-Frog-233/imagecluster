#!bin/bash

cat ${PWD}/requirements.txt | while read line
do
    pip install --user $line
done