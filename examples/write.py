#!/usr/bin/env python

import signal
import time
import sys

from rc522 import RFID

run = True
rdr = RFID()
util = rdr.util()
util.debug = False

#name = input("Name: ")
#department = input("Department: ")
#emp_id = input("Employee ID: ")



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
        
        
        # each card has 16 sectors 0 - 15
        # sector 0 holds manufacturer data and may or may not be writable
        # each sector is protected by two different keys, called A and B
        # each sector has 4 blocks
        # each block holds 16 bits
        # each bit can be from 0 to 255 from the unicode chart
        
        # simple string of text 16 bits long
        new_data = "   coolstuff    "
        # declare array to hold unicode values
        data = []
        # counter for where to insert into array
        i = 0
        # iterate threw the simple string to convert each char into unicode
        for char in new_data:
        	   # add the new unicode code to the data array
        	   data.insert(i, ord(char))
        	   # move to next place in array for next insert
        	   i += 1

        # display the new array
        print(data)
        # write array to sector2 block1
        util.rewrite(8, data)
        
        
        print("\nReading")
        # read sector2 block1 and display it
        block1 = util.read_out(8)
        print (block1)
        print("\nDeauthorizing")
        util.deauth()

        time.sleep(1)
