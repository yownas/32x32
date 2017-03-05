# 32x32
Just for fun. Small python-script to show text/images on adafruit-32x32-led panels with Raspberry pi.

To run:

* mkfifo FIFO
* nohup tail -F FIFO | sudo python 32x32.py

Send commands:
* echo clr > FIFO

Commands:
* nop - Does nothing
* ctxt <row> - Clear text on row
* clock <row> - Show clock on row
* date <row> - Show date on row
* txt <row> <text> - Set text on row
* rtxt <row> <text> - Replace text on row. (Keeps scrolling position)
* tcol <row> <red> <green> <blue> - Set color on row, color value can be 0..255 or r[:low:high} (random between low-high) or <low>-<high>[:start:step] pulse between low/high
* tspd <row> <speed> - Set scrolling speed (float). Can be negative (scrolls to the left)
* clr - Clear background
* load <image> - Load image to background
* exit - Exit 32x32.
