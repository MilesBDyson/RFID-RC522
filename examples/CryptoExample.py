# -*- coding: utf-8 -*-
import time
from pirc522 import RFID
import pickle


# This example will write a dictionary-like object to a MIFARE Classic
# 1K card using AES-128 encryption in CBC mode.
# On the subsequent read of the card it will decrypt the data and
# recover the object. 

rdr = RFID()
util = rdr.util()
#util.debug = True  # Uncomment to see the magic
PASSWORD = "d3aDB33f"
cipher_len = 0
salt = ""
second_read = False
while True:
    # Wait for tag
    rdr.wait_for_tag()

    # Request tag
    (error, data) = rdr.request()
    if not error:
        print("\nDetected")

        (error, uid) = rdr.anticoll()
        if not error:
            print("Setting tag")
            util.set_tag(uid)
            print("\nAuthorizing")
            #util.auth(rdr.auth_a, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
            util.auth(rdr.auth_b, [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])
            # uses the encrypted load function to write a secure card
            if second_read:
                obj_str = util.dump_decrypted(cipher_len, PASSWORD, salt)
                m1_rec = pickle.loads(obj_str)  # Required to recover object
                print "Recovered Object:"
                print m1_rec
                exit(0)
            else:
                m1 = {
                    "sku":"000000000000",
                    "cid":"xxxxxxxxxxxxxx",
                    "ocode":"aaaaaaaaaaaa",
                    "dcode":"xxxxxxxxxx",
                    "wght":0.0,
                    "checker_id":"xxxxxxxxxx"
                }
                m1_str = pickle.dumps(m1)  # Not strictly required.
                (cipher_len, salt) = util.load(m1_str, True, PASSWORD)
                print "Encrypted Data with password and wrote to tag"
                print("Deauthorizing")
                util.deauth()
                raw_input("Remove tag and press enter")
                second_read = True
                time.sleep(1)
