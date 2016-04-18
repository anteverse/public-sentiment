#!/usr/bin/env bash

cd public-sentiment/
rq worker &> /dev/null &
python worker.py &> /dev/null &
python worker.py &> /dev/null &
python worker.py &> /dev/null &
python worker.py &> /dev/null &
python server.py &> /dev/null &
python app.py 5000 &> /dev/null &