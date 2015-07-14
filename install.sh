mkdir -p /opt/ff
set FF_DIR=/opt/ff
cd $FF_DIR
curl -o "https://raw.githubusercontent.com/nikisix/ff/master/ff.sh"
curl -o "https://raw.githubusercontent.com/nikisix/ff/master/ff.py"
curl -o "https://raw.githubusercontent.com/nikisix/ff/master/README"
cat "alias ff='. $FF_DIR/ff.sh'" >> ~/.bashrc
