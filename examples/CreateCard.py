#!/usr/bin/env python

import signal
import time
import sys
import uuid
from rc522 import RFID
from lcd_i2c import *
import Adafruit_BBIO.GPIO as GPIO

# each card has 16 sectors 0 - 15
# sector 0 holds manufacturer data and may or may not be writable
# each sector is protected by two different keys, called A and B
# each sector has 4 blocks
# each block holds 16 bits
# each bit can be from 0 to 255 from a unicode chart

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

rly1 = "P8_8"
rly2 = "P8_10"
GPIO.setup (rly1, GPIO.OUT )
GPIO.setup (rly2, GPIO.OUT )
GPIO.output (rly1, GPIO.HIGH )
GPIO.output (rly2, GPIO.HIGH )

sector = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[16,17,18,19],[20,21,22,23],[24,25,26,27],[28,29,30,31],[32,33,34,35],[36,37,38,39],[40,41,42,43],[44,45,46,47],[48,49,50,51],[52,53,54,55],[56,57,58,59],[60,61,62,63]]



def relay(pin):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(5)
    GPIO.output(pin, GPIO.HIGH)

def makechar(data):
    text = ''.join(chr(i) for i in data)
    return text

def makeascii(data):
    data = "{:<16}".format(data)
    ascii = []
    i = 0
    for char in data:
        ascii.insert(i, ord(char))
        i += 1
    return ascii

def makeblocks(data):
    block = [(data[i:i+16]) for i in range(0, len(data), 16)]
    return block

def makeuuid():
    unique = str(uuid.uuid4()).replace('-','')
    return unique

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    lcd_byte(0x01, LCD_CMD)
    sys.exit()

signal.signal(signal.SIGINT, end_read)

lcd_init()
while run:
    #print(chr(27) + "[2J")
    lcd_string("Ready..",LCD_LINE_1)
    lcd_string(" ",LCD_LINE_2)
    
    print("Press Enter to exit")
    cardtype = input("Card Type [Master,Super,User]: ")

    if len(cardtype) > 0:
        cardtype = cardtype[:16]
    else:
        run = False
        rdr.cleanup()
        lcd_byte(0x01, LCD_CMD)
        break
    fname = input("First Name [Max 48 Char]: ")
    lname = input("Last Name [Max 48 Char]:")
    empid = input("Employee ID [Max 16 Char]:")
    depnum = input("Department Number [Max 16 Char]:")
    title = input("Title [Max 16 Char]: ")
    
    print ("Waiting for Tag...\n")
    lcd_string("Waiting for Tag...",LCD_LINE_1)
    rdr.wait_for_tag()

    (error, data) = rdr.request()
    (error, uid) = rdr.anticoll()
    if not error:
        
        card_id = "UID: "+str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
        #lcd_string(card_id,LCD_LINE_1)
        
        # Setting tag
        util.set_tag(uid)
        
        # Authorizing
        util.auth(rdr.auth_a, [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])
        #util.auth(rdr.auth_a, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
        #util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])

        cardtype = makeascii(cardtype)
        util.rewrite(sector[2][0],cardtype)
        
        uniqueid = makeblocks(makeuuid())
        uniqueid1 = makeascii(uniqueid[0])
        util.rewrite(sector[2][1],uniqueid1)
        uniqueid2 = makeascii(uniqueid[1])
        util.rewrite(sector[2][2],uniqueid1)
        
        #fname = fname[:48]
        fname = "{:<48}".format(fname)
        fname = makeblocks(fname)
        fnameb1 = makeascii(fname[0])
        util.rewrite(sector[3][0],fnameb1)
        fnameb2 = makeascii(fname[1])
        util.rewrite(sector[3][1],fnameb2)
        fnameb3 = makeascii(fname[2])
        util.rewrite(sector[3][2],fnameb3)
        
        #lname = lname[:48]
        lname = "{:<48}".format(lname)
        lname = makeblocks(lname)
        lnameb1 = makeascii(lname[0])
        util.rewrite(sector[4][0],lnameb1)
        lnameb2 = makeascii(lname[1])
        util.rewrite(sector[4][1],lnameb2)
        lnameb3 = makeascii(lname[2])
        util.rewrite(sector[4][2],lnameb3)
        
        empid = "{:<16}".format(empid)
        empid = makeblocks(empid)
        empid = makeascii(empid[0])
        util.rewrite(sector[5][0],empid)
        
        depnum = "{:<16}".format(depnum)
        depnum = makeblocks(depnum)
        depnum = makeascii(depnum[0])
        util.rewrite(sector[5][1],depnum)
        
        title = "{:<16}".format(title)
        title = makeblocks(title)
        title = makeascii(title[0])
        util.rewrite(sector[5][2],title)
        
        unique = makeuuid()+makeuuid()
        unique = makeblocks(unique)
        unique1 = makeascii(unique[0])
        util.rewrite(sector[15][0],unique1)
        unique2 = makeascii(unique[1])
        util.rewrite(sector[15][1],unique2)
        unique3 = makeascii(unique[2])
        util.rewrite(sector[15][2],unique3)
        
        print("Card Created Successfully")

        util.deauth()
        time.sleep(5)
