#!/bin/bash

docker build -t awale .
docker run -it --rm -p 5900:5900 awale