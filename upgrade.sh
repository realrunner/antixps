#!/bin/sh

service antixps stop
git pull
sleep 1
service antixps start