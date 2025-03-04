#!/bin/sh

if ! pip show termgraph &> /dev/null; then
    pip install termgraph
fi

termgraph data.dat --color {blue,magenta}