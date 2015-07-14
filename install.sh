mkdir -p /opt/ff
set FF_DIR=/opt/ff
cd $FF_DIR
curl -O "https://raw.githubusercontent.com/nikisix/ff/master/ff.sh"
curl -O "https://raw.githubusercontent.com/nikisix/ff/master/ff.py"
curl -O "https://raw.githubusercontent.com/nikisix/ff/master/README"
cat 'alias ff=". /opt/ff/ff.sh"' >> ~/.bashrc
