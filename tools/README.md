# Tools
this directory contains a few tools for working with the MIFARE 1k rfid card, it is recommended you understand the read and write fucntions as well as understanding the access bits and how they work before using any of the key changing tools in this directory.

# KeyChange
this will change the default key used to read and write, please read the comments before running

# DefKeyChange
this will reset the key back to default, please read the comments before running

# RandomKeyGen
this is a simple stand alone program that will generate some random keys you can use in your projects, it also is commented if you wish to modfy its ouput in some way, this program will create a new text file in the directory it is executed in and contain the new random keys, if your project uses multiple keys it is recomended that you use this file to keep track of them and there uses. this will help make things a bit easier for you when developing.
