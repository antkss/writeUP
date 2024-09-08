#!/bin/sh

socat tcp-listen:9001,fork,reuseaddr exec:/app/git 2>/dev/null