#!/bin/bash
FF_DIR=~/.ff
mkdir $FF_DIR
cd $FF_DIR
curl -O "https://raw.githubusercontent.com/nikisix/ff/master/ff.sh"
curl -O "https://raw.githubusercontent.com/nikisix/ff/master/ff.py"
curl -O "https://raw.githubusercontent.com/nikisix/ff/master/README"
echo "alias ff='. $FF_DIR/ff.sh'" >> ~/.bashrc
source ~/.bashrc
