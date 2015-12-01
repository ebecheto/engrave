#! /usr/bin/python

import sys
import argparse

parser = argparse.ArgumentParser(description='echo "FOO_B@R" | alphNum2gcode.py generates gcode of the letters to be used with the laser engrave machine')
parser.add_argument('-sx', type=float, default=1.0, help='sx scale, 1.0 if not specified')
parser.add_argument('-sy', type=float, help='sy scale = sx if not specified')
args = parser.parse_args()

sy=args.sy if args.sy else args.sx
sx=args.sx

# sx = 2
# sy = 2
ss = 2.0/sx #<== step in X axis after each letters 
ssy = ss

name="AB12gcode"
chars=[]
chars.extend(name)
print "(*",
print chars,
print "*)"

varViewer=True
#Ton='M03 G04 P0.1'+' G0Z0' if varViewer is True else ''
Ton='M03 G04 P0.1'+'G0Z-1' if varViewer is True else ''
Tof='M05'+' G0Z1' if varViewer is True else ''
# OK, TODO, change it to a parameter like, for tool specific purpose

## HOME MADE FONT DEFINITION, will be completed later on
def char2grbl(x):
    return {
        '0':
         """(number 0)
         M03 G04 P0.1 G0Z-1
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
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G0 X{:.3f} Y{:.3f}
         """.format(1*sx, 4*sy, ss*sx, -4*sy),

        '2':
         """(number 2)
         G0 Y{:.3f}
         M03 G04 P0.1 G0Z-1
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
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G0 X{:.3f} Y{:.3f}
         """.format(3*sx, 2*sy, -3*sx, 3*sx, 2*sy, -3*sx, 5*sx, -4*sy),

        '4':
         """(number 4)
         G0 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G0 X{:.3f} Y{:.3f}
         """.format(3*sx, 4*sy, -3*sx, -2*sy, 3*sx, ss*sx, -2*sy),

        '5':
         """(number 5)
         M03 G04 P0.1 G0Z-1
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
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         G1 Y{:.3f}
         M05G0Z1
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G0 X {:.3f} Y{:.3f}
         """.format(3*sx, 2*sy, -3*sx, -2*sy, 2*sy, 2*sy, 3*sx, ss*sx, -4*sy),

        '7':
         """(number 7)
         G0 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G0 X{:.3f} Y{:.3f}
         """.format(1*sx, 2*sx, 4*sy, -3*sx, (3+ss)*sx, -4*sy),

        '8':
         """(number 8)
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         G1 Y{:.3f}
         M05G0Z1
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G0 X{:.3f} Y{:.3f}
         """.format(3*sx, 4*sy, -3*sx, -4*sy, 2*sy, 3*sx, ss*sx, -2*sy),

        '9':
         """(number 9)
         M03 G04 P0.1 G0Z-1
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
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         M05G0Z1
         G1 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, 1.5*sx, 0.0*sx, -2*sy, 0.0*sx, -1*sy, -1.5*sx, 2*sx, 0.0*sx, -2*sy, 0.0*sx, -1*sy, -2*sx, (ss+3)*sx),

        'C': 
         """(letter C : tan 60=0.32)
         G1 X{:.3f} Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(3*sx, 0.32*sy, 0.0*sx, 3.36*sy, -1.0*sx, 1.68*sy, ss*sx, -3.68*sy),

        'D': 
         """(letter D)
         M03 G04 P0.1 G0Z-1
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
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format( 3*sx, 4*sy, -3*sx, -2*sy, 2*sx, -2*sx, -2*sy, 3*sx, ss*sx),

        'F': 
         """(letter F)
         G1 X{:.3f} Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format( 3*sx, 4*sy, -3*sx, -2*sy, 2*sx, -2*sx, -2*sy, (3+ss)*sx),

        'G': 
         """(letter G : tan60=0.32)
         G1 X{:.3f} Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(3*sx, 3.68*sy, 0.0*sx, -3.36*sy, -1.5*sx, -1.68*sy, 1.68*sy, -1.5*sx, (ss+1.5)*sx, -2*sy),

        'H': 
         """(letter H)
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, -2*sy, 3*sx, 2*sy, -4*sy, ss*sx),

        'I': 
         """(letter I)
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(3*sx, 4*sy, -3*sx, 1.5*sx, -4*sy, (1.5+ss)*sx),

        'J': 
         """(letter J)
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(1.5*sy, 3*sx, 0.0*sy, 1.5*sx, 0.0*sx, 2.5*sy, -2*sx, (2+ss)*sx, -4*sy),

        'K': 
         """(letter K)
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, 3*sx, -3*sx, -2*sy, 3*sx, -2*sy, ss*sx),

        'L': 
         """(letter L)
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, -4*sy, 3*sx, ss*sx),

        'M': 
         """(letter M)
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, 1.5*sx,-2*sy, 1.5*sx, 2*sy, -4*sy, ss*sx),

        'N': 
         """(letter N)
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(4*sy, 3*sx, -4*sy, 4*sy, ss*sx, -4*sy),

        'O': 
         """(letter O)
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 Y{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(1.5*sy, 1*sy, 3*sx, 0*sy, 1.5*sx, 0*sy, -1*sy, -3*sx, 0*sy, -1.5*sx, 0*sy , (3+ss)*sx, -1.5*sy),

        'P': 
         """(letter P)
         M03 G04 P0.1 G0Z-1
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
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 Y{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         M05G0Z1
         G1 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(1.5*sy, 1*sy, 3*sx, 0*sy, 1.5*sx, 0*sy, -1*sy, -3*sx, 0*sy, -1.5*sx, 0*sy, 1.5*sx, 1.5*sx, -1.5*sy, ss*sx),

        'R': 
         """(letter R)
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, 2*sx, 0*sx, -2*sy, 0*sx, -1*sy, -2*sx, 1*sx, 2*sx, -2*sy, (3+ss)*sx),

        'R': 
         """(letter R)
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         G1 X{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, 2*sx, 0*sx, -2*sy, 0*sx, -1*sy, -2*sx, 1*sx, 2*sx, -2*sy, ss*sx),

        'S': 
         """(letter S)
         M03 G04 P0.1 G0Z-1
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
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(1.5*sx, 4*sy, -1.5*sx, 3*sx, ss*sx, -4*sy),

        'U': 
         """(letter U)
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f} 
         M05G0Z1
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(4*sy, -2.5*sy, 3*sx, 0*sy, 1.5*sx, 0*sy, 2.5*sy, -4*sy, ss*sx),

        'V': 
         """(letter V)
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(4*sy, 1.5*sx, -4*sy, 1.5*sx, 4*sy, ss*sx, -4*sy),

        'W': 
         """(letter W)
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(4*sy, 0.75*sx, -4*sy, 0.75*sx, 3*sy, 0.75*sx, -3*sy, 0.75*sx, 4*sy, ss*sx, -4*sy),

        'X': 
         """(letter X)
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(3*sx, 4*sy, -3*sx, 3*sx, -4*sy, ss*sx),

        'Y': 
         """(letter Y : `/)
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(3*sx, 4*sy, -3*sx, 1.5*sx, -2*sy, (1.5+ss)*sx, -2*sy),

        'Z': 
         """(letter Z)
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
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
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f}
         """.format(3*sx, ss*sx),

        '-': 
         """(letter minus)
         G1 X{:.3f} Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(0.5*sx, 2*sy, 2*sx, (0.5+ss)*sx, -2*sy),

        '=': 
         """(letter equal)
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(1.5*sy, 3*sx, 1*sy, -3*sx, (3+ss)*sx, -2.5*sy),

        '/': 
         """(divided)
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(3*sx, 4*sy, ss*sx, -4*sy),

        '*': 
         """(mult)
         G1 X{:.3f} Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(0.5*sx, 2.5*sy, 2*sx, 1*sy, -1*sx, -1.5*sy, 2*sy, -1*sx, -0.5*sy, 2*sx, -1*sy, (0.5+ss)*sx, -2.5*sy, ),

        '%': 
         """(percent 0/o)
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f} Y{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G2 X0Y0I0 J{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         M03 G04 P0.1 G0Z-1
         G2 X0Y0I0 J{:.3f}
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(3*sx, 4*sy, -2*sx, -0.25*sy, -0.75*sy, 1*sx, -2*sy, -0.75*sy , (1+ss)*sx, -1.75*sy),

        '@': 
         """(@ at)
         G1 X{:.3f}
         M03 G04 P0.1 G0Z-1
         G1 X{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f}
         G2 X{:.3f} Y{:.3f} I{:.3f} J{:.3f}
         G2 X0Y0I{:.3f} J0
         M05G0Z1
         G1 X{:.3f} Y{:.3f}
         """.format(2*sx, -0.5*sx , 1.5*sx, 1.5*sy, 0*sx, 1.5*sy, -1*sx, 0*sy, -0.5*sx, 0*sy, -0.5*sx, (1.5+ss)*sx, -1.5*sy),

        '$': 
         """(easter egg round square wrap up)
         M03 G04 P0.1 G0Z-1
         G1 Y{:.3f}
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f}
         G1 X{:.3f}
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f}
         G1 Y{:.3f}
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f}
         G1 X{:.3f}
         G3 X{:.3f} Y{:.3f} I{:.3f} J{:.3f}
         M05G0Z1
         """.format(4*sy , -ss*sx, ss*sy, -ss*sx, 0*sy, -NBE*5*sx, -ss*sx, -ss*sy,0*sx, -ss*sy, -4*sy, ss*sx, -ss*sy, ss*sx, 0*sy,NBE*5*sx,ss*sx, ss*sy, 0*sx, ss*sy),

    }.get(x, "({} not yet defined)".format(x))



def printGrblFromString(str):
    for char in str:
        print(char2grbl(char))

def line2grbl(line):
    lines = line.split('\n')
# TODO : return every \n with len(line) characters*(3*sx+ss)
#    [ [line, len(line)] for line in lines.split('\n') ]
    for s in lines[0:-1]:
        print("("+s+")")
        printGrblFromString(s)
        print "G1 X{:.3f} Y{:.3f}".format(-len(s)*(3+ss)*sx, -(4*sy+ssy))
    printGrblFromString(lines[-1])


print("G91\nF500\ng21") # <== a mettre dans un header

#stdinString=raw_input()
stdinString=sys.stdin.read()[0:-1]  # remove EOF
NBC=len(stdinString)
NBE=NBC-1 #<== number of character minus easter character
#printGrblFromString(stdinString)
line2grbl(stdinString)
print("({}-char to engrave)".format(NBC))
