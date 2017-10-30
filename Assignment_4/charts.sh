#!/bin/bash

#FILE = "/ilab/users/jl1806/cs417/Assignment_4/output.txt"

rm output.txt; touch output.txt;

for i in 1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 65535
do
    echo "python client.py ls.cs.rutgers.edu 50790 udp stop-and-wait $i"
    #python client.py ls.cs.rutgers.edu 50790 udp stop-and-wait $i
    python client.py ls.cs.rutgers.edu 50790 tcp stop-and-wait $i >> "output.txt"
done
