#!/bin/bash

#FILE = "/ilab/users/jl1806/cs417/Assignment_4/output.txt"

for i in 1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 32768 65536
do
    python client.py localhost 50790 tcp pure-streaming $i >> "output.txt"
done
