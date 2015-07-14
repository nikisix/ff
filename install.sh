#!/bin/bash
FF_DIR=~/.ff
mkdir $FF_DIR
cd $FF_DIR
curl -O "https://raw.githubusercontent.com/nikisix/ff/master/ff.sh"
curl -O "https://raw.githubusercontent.com/nikisix/ff/master/ff.py"
curl -O "https://raw.githubusercontent.com/nikisix/ff/master/README"
echo "alias ff='. $FF_DIR/ff.sh'" >> ~/.bashrc
chmod 775 $FF_DIR/ff.py $FF_DIR/ff.sh
#http://stackoverflow.com/questions/670191/getting-a-source-not-found-error-when-using-source-in-a-bash-script
. ~/.bashrc #must be '.' not source. '.' is for bash, source is for csh
