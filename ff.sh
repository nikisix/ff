#FF_DIR=/opt/ff
# FF_USER=`id | sed 's/[^(]*(//;s/).*//'`
# FF_PWD_DIR="${TMPDIR-/tmp}ff-$FF_USER"
# mkdir -p $FF_PWD_DIR
# FF_TEMP_FILE="$FF_PWD_DIR/ff.pwd.$$"
FF_DIR="~/.ff"
FF_TEMP_FILE="$FF_DIR/ff_temp.txt"
touch $FF_TEMP_FILE
python $FF_DIR/ff.py "$FF_TEMP_FILE" "$@"

if test -r "$FF_TEMP_FILE"; then
        FF_PWD="`cat "$FF_TEMP_FILE"`"
        if test -n "$FF_PWD" && test -d "$FF_PWD"; then
                cd "$FF_PWD"
        fi
        unset FF_PWD
fi

rm -f "$FF_TEMP_FILE"
unset FF_TEMP_FILE
