#!/usr/bin/env python

import signal
import time
import sys
import uuid
from pirc522 import RFID
from lcd_i2c import *
import Adafruit_BBIO.GPIO as GPIO

# each card has 16 sectors 0 - 15
# sector 0 holds manufacturer data and may or may not be writable
# each sector is protected by two different keys, called A and B
# each sector has 4 blocks
# each block holds 16 bits
# each bit can be from 0 to 255 from the ascii chart

# Sector 0  ==  Reserved
# Sector 1  ==  Key
# Sector 2  ==  Card Type  [master,super,user][16 char], UUID [32 char]
# Sector 3  ==  First Name  [Max 48 char]
# Sector 4  ==  Last Name  [max 48 char]
# Sector 5  ==  employee id [16 char], department number [16 char], title [16 char]
# Sector 6  ==  status [in,out][16 char]
# Sector 7  ==  
# Sector 8  ==
# Sector 9  == 
# Sector 10  ==
# Sector 11  ==
# Sector 12  ==
# Sector 13  ==
# Sector 14  ==
# Sector 15  ==  Unique string [generated 48 char]





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

relay(rly1)
exit()


lcd_init()
while run:
    #print(chr(27) + "[2J")
    lcd_string("Ready..",LCD_LINE_1)
    lcd_string(" ",LCD_LINE_2)
    
    
    cardtype = input("Card Type [Master,Super,User]: ")

    if len(cardtype) > 0:
        cardtype = cardtype[:16]
    else:
        run = False
        rdr.cleanup()
        lcd_byte(0x01, LCD_CMD)
        break
    
    cardtype = makeascii(cardtype)
    uniqueid = makeblocks(makeuuid())
    uniqueid1 = makeascii(uniqueid[0])
    uniqueid2 = makeascii(uniqueid[1])
    fname = input("First Name: ")
    fname = fname[:16]
    fname = makeascii(fname)
    lname = input("Last Name: ")
    lname = lname[:16]
    lname = makeascii(lname)
    empid = input("Employee ID: ")
    empid = empid[:16]
    empid = makeascii(empid)
    depnum = input("Department Number: ")
    depnum = depnum[:16]
    depnum = makeascii(depnum)
    title = input("Title: ")
    title = title[:16]
    title = makeascii(title)
    

    unique = makeuuid()+makeuuid()
    unique = makeblocks(unique)
    unique1 = makeascii(unique[0])
    unique2 = makeascii(unique[1])
    unique3 = makeascii(unique[2])

    
    
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

        lcd_string(makechar(cardtype),LCD_LINE_1)
        lcd_string(makechar(fname),LCD_LINE_2)



        # write array to sector2 block1
        #util.rewrite(8, data)
        #data = makeascii(cardtype)
        #util.rewrite(sector[1][0],data)
        
        # read sector2 block1 and display it
        #block1 = util.read_out(8)
        #print (block1)
        typecard = util.read_out(sector[1][0])
        text = makechar(typecard)
        print (text)
        
        print("\nDeauthorizing")
        util.deauth()

        time.sleep(5)
