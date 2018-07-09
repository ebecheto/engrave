# engrave

Inspired from sream.py and simple_stream.py, we tuned it so that we could piped text from command line instead of using the software provided with the laser engraver.

We added a 'very basic home made font' using arc code G02 G03 if possible.
For more advanced text font/ picture to engrave, we prefere the use of inkscape.

Our prefered setup is to use the raspberry pi connected to the arduino nano of the engraver machine via USB.


``` shell
# code example
echo "F@BL@B$" |./alphNum2gcode.py |./streamin.py /dev/ttyUSB1 
echo -n "line1\nline2" |./alphNum2gcode.py |./streamin.py /dev/ttyUSB1 

```

When generating a gcode with inskscapte, we need to remove the comment from the file, because they are not removed with streamin.py ==> sed substitue parenthesis and any character after with nothing.

```
cat ReineDesCrepes_floc3.ngc |sed -e 's/(.*//g' | ~/git/engrave/streamin.py /dev/ttyUSB0 
```




![synoptique setup](./engraveSynoptique2.jpg)





``` shell
$ ./alphNum2gcode.py --help
usage: alphNum2gcode.py [-h] [-sx SX] [-sy SY] [-ss SS] [-ssy SSY] [-feed FEED]

echo "FOO_B@R" | alphNum2gcode.py generates gcode of the letters to be used with
the laser engrave machine

optional arguments:
  -h, --help  show this help message and exit
  -sx SX      sx scale, 1.0 if not specified
  -sy SY      sy scale = sx if not specified
  -ss SS      ss : spacing between char, default=2.0/sx
  -ssy SSY    newline space, default = ss
  -feed FEED  feed to gcode : F{feed} default 500
```

USAGE examples :

echo -e -n  'HELLO\n\nWORLD!$' | ./alphNum2gcode.py -ssy=4
echo -e -n 'X__\nX0_\nX[]' | ./alphNum2gcode.py  -ss=0 -ssy=0 -feed 1000  | ./streamin.py 