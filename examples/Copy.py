#!/usr/bin/env python

import signal
import time
import sys

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
    sys.exit()


def read_card():
    rdr.wait_for_tag()
    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))
    (error, uid) = rdr.anticoll()
    bKeyValue = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
    if not error:
        print("Card read UID {:02x}{:02x}{:02x}{:02x}: ".format(uid[0], uid[1], uid[2], uid[3]))
        if not rdr.select_tag(uid):
            for i in range(16):
                if not rdr.card_auth(rdr.auth_b, i * 4 + 3, bKeyValue, uid):
                    for j in range(4):
                        print("data for block {} : ".format(i * 4 + j))
                        ret, data = rdr.read(i * 4 + j)
                        tempCardData.append(data)
                        if not ret:
                            print(data)
                        else:
                            print("read error ... ")
                else:
                    print("card auth failed!")
        else:
            print("select tag failed! ")


def copy_card(dt):
    rdr.wait_for_tag()
    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))
    (error, uid) = rdr.anticoll()
    bKeyValue = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
    if not error:
        print("Card read UID {:02x}{:02x}{:02x}{:02x}: ".format(uid[0], uid[1], uid[2], uid[3]))
        if not rdr.select_tag(uid):
            for i in range(16):
                if i == 0:
                    print("try to write block {}".format(dt[0]))
                    ret = rdr.write(0, dt[0])
                    if not ret:
                        print("write block success")
                    else:
                        print("write error ... ")

                    if not rdr.card_auth(rdr.auth_b, i * 4 + 3, bKeyValue, uid):
                        for j in range(1, 4):
                            ret = rdr.write(i * 4 + j, dt[i * 4 + j])

                            print("try to write block {}".format(dt[i * 4 + j]))
                            if not ret:
                                print("write block success")
                            else:
                                print("write error ... ")
                    else:
                        print("card auth failed!")
                else:
                    if not rdr.card_auth(rdr.auth_b, i * 4 + 3, bKeyValue, uid):
                        for j in range(4):
                            ret = rdr.write(i * 4 + j, dt[i * 4 + j])

                            print("try to write block {}".format(dt[i * 4 + j]))
                            if not ret:
                                print("write block success")
                            else:
                                print("write error ... ")
                    else:
                        print("card auth failed!")
        else:
            print("select tag failed! ")

signal.signal(signal.SIGINT, end_read)

print("Starting")
tempCardData = []
while run:
    action = "1"
    if len(tempCardData) > 0:
        print("read all data for card : 1  ")
        print("copy {:02x}{:02x}{:02x}{:02x} card : 2  ".format(tempCardData[0][0], tempCardData[0][1],
                                                                tempCardData[0][2], tempCardData[0][3]))
        action = input("input the action you want todo:")
    if action == "1":
        read_card()
    else:
        copy_card(tempCardData)

    time.sleep(1)

    # print("Setting tag")
    # util.set_tag(uid)
    # print("\nAuthorizing")
    # #util.auth(rdr.auth_a, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
    # util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])
    # print("\nReading")
    # util.read_out(4)
    # print("\nDeauthorizing")
    # util.deauth()
    #
    # time.sleep(1)
