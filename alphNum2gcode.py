#! /usr/bin/python

import sys
import argparse

parser = argparse.ArgumentParser(description='echo "FOO_B@R" | alphNum2gcode.py generates gcode of the letters to be used with the laser engrave machine')
parser.add_argument('-sx', type=float, default=1.0, help='sx scale, 1.0 if not specified')
parser.add_argument('-sy', type=float, help='sy scale = sx if not specified')
parser.add_argument('-ss', type=float, help='ss : spacing between char, default=2.0/sx')
parser.add_argument('-ssy', type=float, help='newline space, default = ss ')
args = parser.parse_args()

sy=args.sy if args.sy else args.sx
sx=args.sx
ss = args.ss if args.ss else 2.0/sx #<== step in X axis after each letters 
ssy = args.ssy if args.ssy else ss
#<== number of step of \n for newline goback feature

varViewer=True
#Ton='M03 G04 P0.1'+' G0Z0' if varViewer is True else ''
Ton='M03 G04 P0.1'+'G0Z-1' if varViewer is True else ''
Tof='M05'+' G0Z1' if varViewer is True else ''
# OK, TODO, change it to a parameter like, for tool specific purpose

## HOME MADE FONT DEFINITION, will be completed later on
def char2grbl(x, NBE=2):
    return {
        '0':
         """(number 0 zero)
M03G04P0.1G0Z-1
G1 X{:.3f}
G1 Y{:.3f}
G1 X{:.3f}
G1 Y{:.3f}
M05G0Z1
G0 X{:.3f}
""".format(3*sx, 4*sy, -3*sx, -4*sy, (3+ss)*sx),

        '1':
         """(number 1)
G0 X{:.3f}
M03G04P0.1G0Z-1
G1 Y{:.3f}
M05G0Z1
G0 X{:.3f} Y{:.3f}
""".format(1*sx, 4*sy, ss*sx, -4*sy),

        '2':
         """(number 2)
         G0 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G0 X{:.3f}
         """.format(4*sy, 3*sx, -2*sy, -3*sx, -2*sy, 3*sx, ss*sx),

        '3':
         """(number 3)
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G0 X{:.3f} Y{:.3f}
         """.format(3*sx, 2*sy, -3*sx, 3*sx, 2*sy, -3*sx, (2+ss)*sx, -4*sy),

        '4':
         """(number 4)
         G0 X{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G0 X{:.3f} Y{:.3f}
         """.format(3*sx, 4*sy, -3*sx, -2*sy, 3*sx, ss*sx, -2*sy),

        '5':
         """(number 5)
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G0 X{:.3f} Y{:.3f}
         """.format(3*sx, 2*sy, -3*sx, 2*sy, 3*sx, ss*sx, -4*sy),

        '6':
         """(number 6)
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         G1 Y{:.3f}
         M05G0Z1
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G0 X {:.3f} Y{:.3f}
         """.format(3*sx, 2*sy, -3*sx, -2*sy, 2*sy, 2*sy, 3*sx, ss*sx, -4*sy),

        '7':
         """(number 7)
         G0 X{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G0 X{:.3f} Y{:.3f}
         """.format(1*sx, 2*sx, 4*sy, -3*sx, (3+ss)*sx, -4*sy),

        '8':
         """(number 8)
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         G1 Y{:.3f}
         M05G0Z1
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G0 X{:.3f} Y{:.3f}
         """.format(3*sx, 4*sy, -3*sx, -4*sy, 2*sy, 3*sx, ss*sx, -2*sy),

        '9':
         """(number 9)
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G0 X{:.3f} Y{:.3f}
         """.format(3*sx, 4*sy, -3*sx, -2*sy, 3*sx, ss*sx, -2*sy),

        'A': 
         """(letter A)
         {}
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         {}
         G1 X{:.3f} Y{:.3f}
         {}
         G1 X{:.3f}
         {}
         G0 X{:.3f} Y{:.3f}
         """.format(Ton, 1.5*sx, 4*sy, 1.5*sx, -4*sy, Tof, -2.25*sx, 2*sy,Ton,  1.5*sx, Tof, (ss+0.75)*sx, -2*sy),

        'B': 
         """(letter B)
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         M05G0Z1
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, 1.5*sx, 0.0*sx, -2*sy, 0.0*sx, -1*sy, -1.5*sx, 2*sx, 0.0*sx, -2*sy, 0.0*sx, -1*sy, -2*sx, (ss+3)*sx),

        'C': 
         """(letter C : tan 60=0.32)
         G1 X{:.3f} Y{:.3f}
         M03G04P0.1G0Z-1
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(3*sx, 0.32*sy, 0.0*sx, 3.36*sy, -1.0*sx, 1.68*sy, ss*sx, -3.68*sy),

        'D': 
         """(letter D)
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format( 4*sy, 1*sx, 0*sx, -4*sy, 0.0*sx, -2*sy, -1*sx, (3+ss)*sx),

        'E': 
         """(letter E)
         G1 X{:.3f} Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format( 3*sx, 4*sy, -3*sx, -2*sy, 2*sx, -2*sx, -2*sy, 3*sx, ss*sx),

        'F': 
         """(letter F)
         G1 X{:.3f} Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format( 3*sx, 4*sy, -3*sx, -2*sy, 2*sx, -2*sx, -2*sy, (3+ss)*sx),

        'G': 
         """(letter G : tan60=0.32)
         G1 X{:.3f} Y{:.3f}
         M03G04P0.1G0Z-1
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(3*sx, 3.68*sy, 0.0*sx, -3.36*sy, -1.5*sx, -1.68*sy, 1.68*sy, -1.5*sx, (ss+1.5)*sx, -2*sy),

        'H': 
         """(letter H)
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, -2*sy, 3*sx, 2*sy, -4*sy, ss*sx),

        'I': 
         """(letter I)
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(3*sx, 4*sy, -3*sx, 1.5*sx, -4*sy, (1.5+ss)*sx),

        'J': 
         """(letter J)
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(1.5*sy, 3*sx, 0.0*sy, 1.5*sx, 0.0*sx, 2.5*sy, -2*sx, (2+ss)*sx, -4*sy),

        'K': 
         """(letter K)
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, 3*sx, -3*sx, -2*sy, 3*sx, -2*sy, ss*sx),

        'L': 
         """(letter L)
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, -4*sy, 3*sx, ss*sx),

        'M': 
         """(letter M)
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, 1.5*sx,-2*sy, 1.5*sx, 2*sy, -4*sy, ss*sx),

        'N': 
         """(letter N)
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(4*sy, 3*sx, -4*sy, 4*sy, ss*sx, -4*sy),

        'O': 
         """(letter O)
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 Y{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(1.5*sy, 1*sy, 3*sx, 0*sy, 1.5*sx, 0*sy, -1*sy, -3*sx, 0*sy, -1.5*sx, 0*sy , (3+ss)*sx, -1.5*sy),

        'P': 
         """(letter P)
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(4*sy, 2*sx, 0*sx, -2*sy, 0*sx, -1*sy, -2*sx, (3+ss)*sx, -2*sy),

        'Q': 
         """(letter Q)
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 Y{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         M05G0Z1
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(1.5*sy, 1*sy, 3*sx, 0*sy, 1.5*sx, 0*sy, -1*sy, -3*sx, 0*sy, -1.5*sx, 0*sy, 1.5*sx, 1.5*sx, -1.5*sy, ss*sx),

        'R': 
         """(letter R)
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, 2*sx, 0*sx, -2*sy, 0*sx, -1*sy, -2*sx, 1*sx, 2*sx, -2*sy, (3+ss)*sx),

        'R': 
         """(letter R)
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, 2*sx, 0*sx, -2*sy, 0*sx, -1*sy, -2*sx, 1*sx, 2*sx, -2*sy, ss*sx),

        'S': 
         """(letter S)
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 X{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(2*sx,0*sx,2*sy,0*sx,1*sy,-1*sx, 0*sx,2*sy,0*sx,1*sy, 2*sx, ss*sx, -4*sy),

        'T': 
         """(letter T)
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(1.5*sx, 4*sy, -1.5*sx, 3*sx, ss*sx, -4*sy),

        'U': 
         """(letter U)
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         M05G0Z1
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, -2.5*sy, 3*sx, 0*sy, 1.5*sx, 0*sy, 2.5*sy, -4*sy, ss*sx),

        'V': 
         """(letter V)
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(4*sy, 1.5*sx, -4*sy, 1.5*sx, 4*sy, ss*sx, -4*sy),

        'W': 
         """(letter W)
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(4*sy, 0.75*sx, -4*sy, 0.75*sx, 3*sy, 0.75*sx, -3*sy, 0.75*sx, 4*sy, ss*sx, -4*sy),

        'X': 
         """(letter X)
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(3*sx, 4*sy, -3*sx, 3*sx, -4*sy, ss*sx),

        'Y': 
         """(letter Y : `/)
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(3*sx, 4*sy, -3*sx, 1.5*sx, -2*sy, (1.5+ss)*sx, -2*sy),

        'Z': 
         """(letter Z)
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, 3*sx, -3*sx, -4*sy, 3*sx, ss*sx),

        ' ': 
         """(space)
         G1 X{:.3f}
         """.format((3+ss)*sx),

        '_': 
         """(letter underscore)
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(3*sx, ss*sx),

        '-': 
         """(letter minus)
         G1 X{:.3f} Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(0.5*sx, 2*sy, 2*sx, (0.5+ss)*sx, -2*sy),

        '=': 
         """(letter equal)
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(1.5*sy, 3*sx, 1*sy, -3*sx, (3+ss)*sx, -2.5*sy),

        '/': 
         """(divided)
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(3*sx, 4*sy, ss*sx, -4*sy),

        '*': 
         """(mult)
         G1 X{:.3f} Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(0.5*sx, 2.5*sy, 2*sx, 1*sy, -1*sx, -1.5*sy, 2*sy, -1*sx, -0.5*sy, 2*sx, -1*sy, (0.5+ss)*sx, -2.5*sy, ),

        '%': 
         """(percent 0/o)
         M03G04P0.1G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         M03G04P0.1G0Z-1
         G2 X0Y0I0 J{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         M03G04P0.1G0Z-1
         G2 X0Y0I0 J{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(3*sx, 4*sy, -2*sx, -0.25*sy, -0.75*sy, 1*sx, -2*sy, -0.75*sy , (1+ss)*sx, -1.75*sy),

        '@': 
         """(@ at)
         G1 X{:.3f}
         M03G04P0.1G0Z-1
         G1 X{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f}
         G2 X0Y0I{:.3f} J0
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(2*sx, -0.5*sx , 1.5*sx, 1.5*sy, 0*sx, 1.5*sy, -1*sx, 0*sy, -0.5*sx, 0*sy, -0.5*sx, (1.5+ss)*sx, -1.5*sy),

        '!': 
         """(! bang good?)
         G1 X{:.3f} Y{:.3f}
         M03G04P0.1G0Z-1
         G2 X0Y0I0J{:.3f}
         G1 X{:.3f} Y{:.3f}
         G3 X{:.3f} Y0 I{:.3f} J0
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(1.5*sx, 1*sy, -0.25*sy, 0.5*sx, 2*sy, -1*sx, -0.5*sx, 0.5*sx, -2*sy, (1.5+ss)*sx, -1*sy),

        '$': 
         """(easter egg round square wrap up {:.3f})
         M03G04P0.1G0Z-1
         G1 Y{:.3f}
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f}
         G1 X{:.3f}
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f}
         G1 Y{:.3f}
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f}
         G1 X{:.3f}
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f}
         M05G0Z1
         """.format(NBE, 4*sy , -ss*sx, ss*sy, -ss*sx, 0*sy, -NBE*5*sx, -ss*sx, -ss*sy,0*sx, -ss*sy, -4*sy, ss*sx, -ss*sy, ss*sx, 0*sy,NBE*5*sx,ss*sx, ss*sy, 0*sx, ss*sy),

    }.get(x, "({} not yet defined)".format(x))



def printGrblFromString(str, NBE=2):
    for char in str:
        print(char2grbl(char, NBE))

def line2grbl(inline):
    ast=[ [line, len(line)] for line in inline.split('\n') ]
    NBC=False
    for leaf in ast:
        nbline=0
        if (NBC or leaf[0]=='') :
            print "(goback of {0}-chars)".format(NBC)
            print "G1 X{:.3f} Y{:.3f}".format(-NBC*(3+ss)*sx, -(4*sy+ssy))
        NBC=leaf[1]
        NBE=NBC-1
        print "(NBE="+str(NBE)+")"
        printGrblFromString(leaf[0], NBC-1)


print("G91\nF500\ng21") # <== a mettre dans un header

#stdinString=raw_input()
#stdinString=sys.stdin.read()[0:-1]  # remove EOF
stdinString=sys.stdin.read()
NBE=0
line2grbl(stdinString)
# $> echo -e -n  "AB\nCPH0$" | ./alphNum2gcode.py -ssy=4 > newLines.nc
# echo -e -n  'HELLO\n\nWORLD!$' | ./alphNum2gcode.py -ssy=4 > newLines.nc

