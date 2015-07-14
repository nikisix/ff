FF_USER=`id | sed 's/[^(]*(//;s/).*//'`
FF_PWD_DIR="${TMPDIR-/tmp}ff-$FF_USER"
mkdir -p $FF_PWD_DIR
FF_PWD_FILE="$FF_PWD_DIR/ff.pwd.$$"
touch $FF_PWD_FILE
python ~/code/git/terminal-navigators/ff/ff.py "$FF_PWD_FILE" "$@"

if test -r "$FF_PWD_FILE"; then
        FF_PWD="`cat "$FF_PWD_FILE"`"
        if test -n "$FF_PWD" && test -d "$FF_PWD"; then
                cd "$FF_PWD"
        fi
        unset FF_PWD
fi

rm -f "$FF_PWD_FILE"
unset FF_PWD_DIR
unset FF_PWD_FILE
