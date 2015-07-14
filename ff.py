#!/usr/bin/python
import os
import sys
import termios
import tty
import subprocess
from subprocess import Popen
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

def formatdir(dirlist, position):
    i = 0; ret = []
    for l in dirlist:
        if i == position: ret.append('*[['+l+']]*')
        else: ret.append(l)
        i+=1
    return ret 

if __name__ == '__main__':
    position = 0
    while 1: 
        os.system("clear")
        curdir = os.listdir('.')
        print os.listdir('..')
        print "||||||||||||||||||||||||||||||||||||||||||||||||||\n"
        print os.getcwd()
        print "\n||||||||||||||||||||||||||||||||||||||||||||||||||"
        print formatdir(curdir, position)
        k=inkey()
        if   k == 'q': break
        elif k == 'l': 
            if position < len(curdir)-1: position += 1
        elif k == 'h': 
            if position > 0: position -= 1
        elif k == 'k':
            os.chdir('..')
            position = 0
        elif k == 'j':
            if len(curdir) > 0: #we have some files/directories in this location
                if os.path.isdir('./'+curdir[position]):
                    os.chdir('./'+curdir[position])
                    position = 0
        elif k == '\r':
            os.system("clear")
            print str(os.getcwd())
            with open(sys.argv[1],'w+') as tempfile:
                tempfile.write(os.getcwd())
            #subprocess.Popen(["open", str(os.getcwd)], shell=True)
            #os.system(str("cd "+os.getcwd()))
            break
