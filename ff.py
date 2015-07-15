#!/usr/bin/python
## author nickiVI
## special thanks to danny cansis and John1024@github for tips and pointers along the way
import os
import sys
import termios
import tty
import subprocess
from subprocess import Popen

HELP_MSG="""
 _____         _     _____ _ _           
|  ___|_ _ ___| |_  |  ___(_) | ___  ___ 
| |_ / _` / __| __| | |_  | | |/ _ \/ __|
|  _| (_| \__ \ |_  |  _| | | |  __/\__ \\
|_|  \__,_|___/\__| |_|   |_|_|\___||___/
author: nickiVI 
commands:
h - file left
j - (down) enter dir
k - up dir
l - file right
q - exit without changing dirs
enter - change dir to currently selected and exit
e - preview the file (with less)
"""
# A basic clear screen and cursor removal for program start...
os.system("clear")

# Make any variables global just for this DEMO "game"...
global screen_array
global character
global line
global position
global remember_attributes
global inkey_buffer
global score

screen_array="*"
character="a"
remember_attributes="2015 zen"
line=1
position=0
inkey_buffer=1
score=0
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
def colorize(text, foreground_color):
    CSI="\x1B["
    reset=CSI+"m"
    return CSI + str(fg_colormap[foreground_color])+'m'+text+reset

def format_dir(dirlist):
    for l in dirlist:
        if os.path.isdir('../'+l): print colorize(l,'blue'),
        else: print l,

def format_cur_dir(dirlist, position):
    i = 0;
    for l in dirlist:
        if i == position: print colorize('*[['+l+']]*', 'magenta'),
        else: 
            if os.path.isdir('./'+l): print(colorize(l,'blue')),
            else: print(l),
        i+=1

def move_dir(direction, child, current, parent):
    if direction == 'up':
        child = current
        current = parent
        parent = 0
    elif direction == 'down':
        parent = current
        current = child
        child = 0
    else: print "Error bad direction"
    return (child,current,parent)

if __name__ == '__main__':
    child=0; position = 0; parent=0; 
    while 1: 
        os.system("clear")
        print HELP_MSG
        curdir = os.listdir('.')
        print "PARENT DIR"
        print "||||||||||||||||||||||||||||||||||||||||||||||||||"
        format_dir(os.listdir('..'))
        print "\n||||||||||||||||||||||||||||||||||||||||||||||||||\n"
        print "CURRENT DIR"
        print os.getcwd()
        print "||||||||||||||||||||||||||||||||||||||||||||||||||"
        format_cur_dir(curdir, position)
        print "\n||||||||||||||||||||||||||||||||||||||||||||||||||"
        k=inkey()
        if   k == 'q': break
        elif k == 'l': 
            if position < len(curdir)-1: position += 1
        elif k == 'h': 
            if position > 0: position -= 1
        elif k == 'k':
            #TODO add an index check here to make sure that a new parent is at least as long as the previous parent
            os.chdir('..')
            (child, position, parent) = move_dir('up',child, position, parent)
        elif k == 'j':
            if len(curdir) > 0: #we have some files/directories in this location
                if os.path.isdir('./'+curdir[position]):
                    os.chdir('./'+curdir[position])
                    (child, position, parent) = move_dir('down',child, position, parent)
        elif k == 'e':
            os.system("less "+'./'+curdir[position])
        elif k == '\r':
            os.system("clear")
            print str(os.getcwd())
            with open(sys.argv[1],'w+') as tempfile:
                tempfile.write(os.getcwd())
            #subprocess.Popen(["open", str(os.getcwd)], shell=True)
            #os.system(str("cd "+os.getcwd()))
            break
