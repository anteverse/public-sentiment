#!/usr/bin/env bash

rq worker &> /dev/null &
python worker.py &> /dev/null &
python worker.py &> /dev/null &
python worker.py &> /dev/null &
python worker.py &> /dev/null &
python server.py &> /dev/null &
python app.py 5000 &> /dev/null &