#!/usr/bin/env python

import signal
import time

from rc522 import RFID

run = True
rdr = RFID()
util = rdr.util()
util.debug = True

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()

signal.signal(signal.SIGINT, end_read)

print("Starting")
while run:
    rdr.wait_for_tag()

    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))

    (error, uid) = rdr.anticoll()
    if not error:
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

        print("Setting tag")
        util.set_tag(uid)
        print("\nAuthorizing")
        util.auth(rdr.auth_a, [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])
        print("\nWriting modified bytes")
        util.rewrite(4, [None, None, 0x69, 0x24, 0x40])
        util.read_out(4)
        """
        print("\nWriting zero bytes")
        util.rewrite(2, [None, None, 0, 0, 0])
        util.read_out(2)
        print("\nDeauthorizing")
        util.deauth()
        """
        # this line will write a new key that will be permanent and not be reversible so make sure you know what your doing 
        # please see this calculator for setting up the access bits when changing keys and how they are accessed and protected
        # calculator: http://calc.gmss.ru/Mifare1k/ 
        #util.write_trailer(1, (0x12, 0x34, 0x56, 0x78, 0x96, 0x92), (0x0F, 0x07, 0x8F), 105, (0x74, 0x00, 0x52, 0x35, 0x00, 0xFF))
        # this line will write a new key that will be reversible or changeable and is recommended for development and learning purposes
        util.write_trailer(1, (0x12, 0x34, 0x56, 0x78, 0x96, 0x92), (None, None, None), 105, (0x74, 0x00, 0x52, 0x35, 0x00, 0xFF))
        
        util.deauth()
        time.sleep(1)

