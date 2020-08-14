#!/bin/sh
echo "var BACKEND_PORT = $1;" > frontend/prebundle/config.js
cd frontend
python static.py $2
