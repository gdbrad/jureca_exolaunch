#!/bin/bash

for j in `seq 12958207 12958289` ; do
    scancel $j
    echo $j
done
