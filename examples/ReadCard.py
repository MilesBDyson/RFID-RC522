#!/usr/bin/env python

import signal
import time
import sys
from rc522 import RFID

# Sector 0  ==  Reserved
# Sector 1  ==  
# Sector 2  ==  Card Type  [master,super,user][16 char], UUID [32 char]
# Sector 3  ==  First Name  [Max 48 char]
# Sector 4  ==  Last Name  [Max 48 char]
# Sector 5  ==  employee id [Max 16 char], department number [16 char], title [16 char]
# Sector 6  ==  
# Sector 7  ==  
# Sector 8  ==
# Sector 9  == 
# Sector 10  ==
# Sector 11  ==
# Sector 12  ==
# Sector 13  ==
# Sector 14  ==
# Sector 15  ==  Unique string [generated 48 char] can be modified on each swipe and kept track of in a database for additional security if desired

run = True
rdr = RFID()
util = rdr.util()
util.debug = False

sector = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[16,17,18,19],[20,21,22,23],[24,25,26,27],[28,29,30,31],[32,33,34,35],[36,37,38,39],[40,41,42,43],[44,45,46,47],[48,49,50,51],[52,53,54,55],[56,57,58,59],[60,61,62,63]]

def makechar(data):
    text = ''.join(chr(i) for i in data)
    return text

def makeunicode(data):
    data = "{:<16}".format(data)
    unicode = []
    i = 0
    for char in data:
        unicode.insert(i, ord(char))
        i += 1
    return unicode

def makeblocks(data):
    block = [(data[i:i+16]) for i in range(0, len(data), 16)]
    return block

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)


while run:
    print(chr(27) + "[2J")
    print("Waiting for card")
    rdr.wait_for_tag()

    (error, data) = rdr.request()
    (error, uid) = rdr.anticoll()
    if not error:
        util.set_tag(uid)
        util.auth(rdr.auth_a, [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])
        #util.auth(rdr.auth_a, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
        #util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])
        
        cardtype = util.read_out(sector[2][0])
        cardtype = makechar(cardtype)
        print("Card Type: "+cardtype)
        
        uniqueid1 = util.read_out(sector[2][1])
        uniqueid1 = makechar(uniqueid1)
        uniqueid2 = util.read_out(sector[2][2])
        uniqueid2 = makechar(uniqueid2)
        uniqueid = uniqueid1+uniqueid2
        print("UUID: "+uniqueid)
        
        fname1 = util.read_out(sector[3][0])
        fname1 = makechar(fname1)
        fname2 = util.read_out(sector[3][1])
        fname2 = makechar(fname2)
        fname3 = util.read_out(sector[3][2])
        fname3 = makechar(fname3)
        fname = fname1+fname2+fname3
        print("First Name: "+fname)
        
        lname1 = util.read_out(sector[4][0])
        lname1 = makechar(lname1)
        lname2 = util.read_out(sector[4][1])
        lname2 = makechar(lname2)
        lname3 = util.read_out(sector[4][2])
        lname3 = makechar(lname3)
        lname = lname1+lname2+lname3
        print("Last Name: "+lname)
        
        empid = util.read_out(sector[5][0])
        empid = makechar(empid)
        print("Employee ID: "+empid)
        
        depid = util.read_out(sector[5][1])
        depid = makechar(depid)
        print("Department ID: "+depid)
        
        title = util.read_out(sector[5][2])
        title = makechar(title)
        print("Title: "+title)
        print("\n")
        print("Card Reading Complete")


        util.deauth()
        time.sleep(5)
