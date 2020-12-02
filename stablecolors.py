#!/usr/bin/python3

import sacn
import time
import sys
import getopt

debug = 1

#     Type     Uni Num Pixels
pixels = [
    ["icicle", 1, 180],["icicle", 2, 180],
    ["icicle", 3, 120],["ledstrand", 4, 144],
    ["ledstrand", 5, 144],["ledstrand", 6, 144],
    ["ledstrand", 7, 144],["megatree", 10, 100],
    ["megatree", 11, 100],["megatree", 12, 100],["megatree", 13, 100]
]

dmxreceiver = "192.168.244.1"

startuniverse = pixels[0][1]
enduniverse = pixels[(len(pixels)-1)][1]

def stable(color):

    sender = sacn.sACNsender()
    sender.start()

    if color == "white":
        dmxcolor = (255,147,41)
        singlecolor = 1
    elif color == "green":
        dmxcolor = (0,255,0)
        singlecolor = 1 
    elif color == "red":
        dmxcolor = (255,0,0)
        singlecolor = 1
    elif color == "blue":
        dmxcolor = (0,0,255)
        singlecolor = 1
    elif color == "redgreen":
        dmxcolor = (0,255,0,255,0,0)
        singlecolor = 0
    else:
        usage()
        sender.stop()
        sys.exit()

    for universe in range(startuniverse,(enduniverse)+1):
        sender.activate_output(universe) 
        sender[universe].destination = dmxreceiver
   
    for pixel in range(0, len(pixels)):
        pixeltype = pixels[pixel][0]
        universe = pixels[pixel][1]
        numpixels = pixels[pixel][2]

        if singlecolor == 1:
            dmxdata = (dmxcolor * int(numpixels))
        else:
            dmxdata = (dmxcolor * int(numpixels/2))
        
        if debug == 1:
            print('Pixeltype: %s, Universe: %s, Numpixels: %s, Color: %s, DMXColor: %s' % (pixeltype,universe,numpixels,color, dmxcolor))
                    
        sender[universe].dmx_data = dmxdata

    sender.manual_flush = False
    time.sleep(1)
    sender.stop()
    sys.exit()

def usage():
    print('stable.py -h -c <color>')
    print('Implemented colors: white, red, green, blue, redgreen')
    sys.exit()

def main(argv):

    try:
        opts, args = getopt.getopt(argv, "c:")
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt in ("-h"):
            usage()
        elif opt in ("-c"):
            color = arg

    stable(color)

if __name__ == "__main__":
   main(sys.argv[1:])
