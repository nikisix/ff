mkdir -p /opt/ff
set FF_DIR=/opt/ff
cd $FF_DIR
curl -o "https://github.com/nikisix/ff/ff.sh"
curl -o "https://github.com/nikisix/ff/ff.py"
curl -o "https://github.com/nikisix/ff/README"
cat "alias ff='. $FF_DIR/ff.sh'" >> ~/.bashrc
