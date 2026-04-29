#!/bin/bash
# Test claude startup as kerry_back
export HOME=/home/kerry_back
export USER=kerry_back
source /home/kerry_back/.bashrc
cd /home/kerry_back/workspace
claude --print "hello" 2>&1 | head -30
