#! /usr/bin/python

import re
import sys



def load_font(font_file, size, spacing):
    font = {}
    with open(font_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
               continue
            match = re.match(r"CHR_(\w+) (\d+); (.*)", line)
            char_value =  int(match.group(1), 16)
            width = int(match.group(2))
            segments = match.group(3).split(";")
            segments= map(lambda s: s.split(), segments)
            gcode = "G92 x0y0\n"
            for draw in segments:
                # go to first point of draw and start laser
                x, y = map(float, draw[0].split(','))
                gcode += "G1 X{:.3f} Y{:.3f}\n".format(x*size,y*size)
                gcode += "M3 G4 P.1 G0Z-1\n"
                # go through every points in draw
                for point in draw[1:]:
                    x, y = map(float, point.split(','))
                    gcode += "G1 X{:.3f} Y{:.3f}\n".format(x*size,y*size)
                # stop laser
                gcode += "M5 G0Z1\n"
            gcode += "G1 X{:.3f} Y0\n".format(width*size)       
               
            font[chr(char_value)] = gcode
        font[' '] = "G92 x0y0\nG1 X{:.3f} Y0\n".format(spacing*size)
	return font

def string2grbl(str, font):
    for c in str:
        print(font[c])

font = load_font("CHR_font/default.chr", 1./4, 20)

print "G21"
print "F1000"
string2grbl(raw_input(), font)
