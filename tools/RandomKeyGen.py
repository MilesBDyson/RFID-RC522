#!/usr/bin/env python3

import random
# wewill write all generated keys to the file name below
file = 'randomkeys.txt'
randomkeys = open(file,'a')
# clear the terminal before displaying keys
print(chr(27) + "[2J")
loop = 50   #<--- edit this line for the number of keys you wish to generate
k=0
for randkey in range(loop):
	# define list that will hold the random key
	bit = []
	bit.insert(0,random.randint(0,256))
	bit.insert(1,random.randint(0,256))
	bit.insert(2,random.randint(0,256))
	bit.insert(3,random.randint(0,256))
	bit.insert(4,random.randint(0,256))
	bit.insert(5,random.randint(0,256))
	# define list that will hold the hexadecimal conversion of the random key
	key = []
	i = 0
	for char in bit:
		key.insert(i, hex(char))
		i += 1
	# print to terminal the random key created after converted to hexadecimal
	print (key)
	i = 0
	k += 1
	# looping threw each key and writing it to the file
	for ele in key:
		i += 1
		if i == 1:
			randomkeys.write('Key'+str(k)+' [')
		randomkeys.write(ele)
		if i < 6:
			randomkeys.write(',')
		if i == 6:
			randomkeys.write(']\n')
			i = 0
randomkeys.close()
# print to terminal a basic reminder of where the new file is and what to use it for
print('\n')
print("A file 'randomkeys.txt' was created in this directory")
print("containing the above keys for future reference")
print('\n')
print('when using multiple keys in any project you should take')
print('care in keeping track of them accordingly, use the file')
print('to keep track by commenting the lines with respect to')
print('there usage')
print('\n')