#!/usr/bin/env bash

HOST=localhost                  #
PORT=5000                       #

curl -XGET "http://$HOST:$PORT/location/-90.262,38.640,3"