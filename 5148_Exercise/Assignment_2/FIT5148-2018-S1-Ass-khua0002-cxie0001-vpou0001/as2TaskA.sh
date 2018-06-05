#!/bin/bash

file="as2TaskA.js"
if [ $# -gt 0 ]; then
  file="$1"
fi

mongoimport -d fit5148_db -c climate --type csv --file ClimateData-Part1.csv --headerline
mongoimport -d fit5148_db -c fire --type csv --file FireData-Part1.csv --headerline
mongo < "$file" 2>&1 | tee as2TaskAOut.txt
#Then drop the database automatically
mongo fit5148_db -eval "db.climate.drop()"
mongo fit5148_db -eval "db.fire.drop()"
echo "\nDone!"