#!/usr/bin/env bash

HOST=localhost                  #
PORT=5000                       #

# coordinates are random
curl -XGET "http://$HOST:$PORT/location/-90.262,38.640,3"
curl -XDELETE "http://$HOST:$PORT/location/-90.262,38.640,3"
curl -XGET "http://$HOST:$PORT/location/"
curl -XPOST "http://$HOST:$PORT/location/" -d '{ "data": "data" }'
curl -XPUT "http://$HOST:$PORT/location/" -d '{ "data": "data" }'