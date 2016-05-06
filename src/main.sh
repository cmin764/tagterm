#! /bin/bash

javac Main.java

if [ $? -eq 0 ]; then
    java Main $1 $2;
fi
