#!/usr/bin/python
## author nickiVI
## special thanks to danny cansis and John1024@github for tips and pointers along the way
import math
import os
import sys
import termios
import tty
import subprocess
from subprocess import Popen

HELP_MSG="""\
 _____         _     _____ _ _              h - file left 
|  ___|_ _ ___| |_  |  ___(_) | ___  ___    j - file down
| |_ / _` / __| __| | |_  | | |/ _ \/ __|   k - file up
|  _| (_| \__ \ |_  |  _| | | |  __/\__ \\  l - file right
|_|  \__,_|___/\__| |_|   |_|_|\___||___/
author: nickiVI 
commands:
q - exit without changing dirs
enter - change dir to currently selected and exit
e - preview the file (with less)"""
# A basic clear screen and cursor removal for program start...
os.system("clear")

#a cross-platform (i hope) way to get terminal size
def terminal_size():
    import fcntl, termios, struct
    #hp - height pixels
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return h, w

# Make any variables global just for this DEMO "game"...
global screen_array
global character
global line
global position
global remember_attributes
global inkey_buffer

screen_array="*"
character="a"
remember_attributes="2015 zen"
line=1
position=0
inkey_buffer=1
def inkey():
    fd=sys.stdin.fileno()
    remember_attributes=termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    character=sys.stdin.read(inkey_buffer)
    termios.tcsetattr(fd, termios.TCSADRAIN, remember_attributes)
    return character

# Color table (wikipedia/ANSI_escape_code). 
# foreground = 30+x  background = 40+x, where x is..
# Intensity	0	1	2	3	4	5	6	7
# Normal	Black	Red	Green	Yellow	Blue	Magenta	Cyan	White
# Bright	Black	Red	Green	Yellow	Blue	Magenta	Cyan	White
# i.e. print CSI+"31;40m" + "Colored Text" + reset + "Non-Colored Text"
colormap = {'black':0,'red':1,'green':2,'yellow':3,'blue':4,'magenta':5,'cyan':6,'white':7}
fg_colormap = {'black':30,'red':31,'green':32,'yellow':33,'blue':34,'magenta':35,'cyan':36,'white':37}
CSI="\x1B["
CSI_Reset=CSI+"m"
def colorize(text, foreground_color):
    return CSI + str(fg_colormap[foreground_color])+'m'+text+CSI_Reset

def color_and_pad_filenames(dirlist, position, rel_level):
    max_file_len = max([len(l) for l in dirlist]) + 2 if len(dirlist) > 0 else 1
    ret=[]; i = 0
    for f in dirlist:
        num_spaces = max_file_len - len(str(f))
        if position==i:    f = colorize(f,'magenta')
        else:    f = colorize(f,'blue') if os.path.isdir('../'*rel_level+f) else f
        ret.append(f+'.'*num_spaces)
        i+=1
    return ret

#rel_level - relative folder level to where you are. 0 is current, 1 is parent
def print2d(dirlist, num_cols, files_per_col,  position=-1, rel_level=0):
    fray = [] #"filearray" 2d array of files in the current directory
    dirlist = color_and_pad_filenames(dirlist, position, rel_level) 
    for i in range(num_cols):  
        start = i*files_per_col
        end   = i*files_per_col+files_per_col if len(dirlist) >= i*files_per_col+files_per_col else len(dirlist)
        if i == num_cols:   end = len(dirlist)
        fray.append(dirlist[start:end])
    max_rows = max([len(a) for a in fray])
    for r in range(max_rows):
        print ''.join([a[r] for a in fray if r<len(a)])

def print_display(num_cols, files_per_col):
    os.system("clear")
    print HELP_MSG
    print "|||PARENT DIR|||||||||||||||||||||||||||||||||||||"
    print2d(os.listdir('..'), num_cols, files_per_col, position=-1, rel_level=1)
    print "||||||||||||||||||||||||||||||||||||||||||||||||||"
    print os.getcwd()
    print "||||CURRENT DIR|||||||||||||||||||||||||||||||||||"
    print2d(os.listdir('.'), num_cols, files_per_col, position=position, rel_level=0)
    print "||||||||||||||||||||||||||||||||||||||||||||||||||"

if __name__ == '__main__':
    child=0; position = 0; parent=0; 
    h, w  = terminal_size()
    while 1: 
        curdir = os.listdir('.')
        #TODO can only see one out of every two directories
        max_file_len = max([len(l) for l in curdir]) if len(curdir) > 0 else 1 #don't divide by 0
        num_cols = int(w/max_file_len)
        files_per_col = int(math.ceil(float(len(curdir))/num_cols))
        print_display(num_cols, files_per_col)
        k=inkey()
        if   k == 'q': break
        elif k == 'l': 
            if position+files_per_col < len(curdir):  position = position+files_per_col
        elif k == 'h': 
            if position-files_per_col >= 0: position = position-files_per_col
        elif k == 'j': 
            if position+1 < len(curdir):  position = position+1
        elif k == 'k': 
            if position-1 >= 0: position = position-1
        elif k == 'f':
            #TODO add an index check here to make sure that a new parent is at least as long as theprevious parent
            os.chdir('..')
            position = len(os.listdir('.'))/2
        elif k == 'd':
            if len(curdir) > 0: #we have some files/directories in this location
                if os.path.isdir('./'+curdir[position]):
                    os.chdir('./'+curdir[position])
                    position = len(os.listdir('.'))/2
        elif k == 'e':
            os.system("less "+'./'+curdir[position])
        elif k == '\r':
            os.system("clear")
            print str(os.getcwd())
            with open(sys.argv[1],'w+') as tempfile:
                tempfile.write(os.getcwd())
            break
