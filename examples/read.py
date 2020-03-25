#!/usr/bin/env python

import signal
import time
import sys

from rc522 import RFID

run = True
rdr = RFID()
util = rdr.util()
util.debug = False

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)

print("Starting")
while run:
    rdr.wait_for_tag()

    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))

    (error, uid) = rdr.anticoll()
    if not error:
        print(chr(27) + "[2J")
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

        print("Setting tag")
        util.set_tag(uid)
        print("\nAuthorizing")
        util.auth(rdr.auth_a, [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])
        #util.auth(rdr.auth_a, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
        #util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])
        print("\nReading")
        
        # get data from sector2 block1
        block1 = util.read_out(8)
        # get data from sector2 block2
        block2 = util.read_out(9)
        # get data from sector2 block3
        block3 = util.read_out(10)
        # get data from sector2 block4
        block4 = util.read_out(11)
        # convert block1 ascii to character
        txt1 = ''.join(chr(i) for i in block1)
        # convert block2 ascii to character
        txt2 = ''.join(chr(i) for i in block2)
        # convert block3 ascii to character
        txt3 = ''.join(chr(i) for i in block3)
        # convert block4 ascii to character
        txt4 = ''.join(chr(i) for i in block4)
        # put all the characters into one string
        text_data = txt1+txt2+txt3
        # display string as characters
        print(text_data)
        
        print("\nDeauthorizing")
        util.deauth()

        time.sleep(1)
