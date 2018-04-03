#!/bin/bash
while read p; do 
	curl -d "text==$p" http://text-processing.com/api/sentiment/
	printf "\n"
done < dictionary2.txt
