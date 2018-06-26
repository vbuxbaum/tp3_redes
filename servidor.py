#!/usr/bin/python3

import socket
import ast
import sys
import json
import time
import struct
import codecs
import threading
import copy
import re

tag_users = {}

def add_tag_users(tag, userIP):
	global tag_users

	if (tag in tag_users):
		if userIP not in tag_users[tag]:
			tag_users[tag].append(userIP)  
	else:
	 	tag_users[tag] = [userIP]

	print (tag_users)

def rm_tag_users(tag, userIP):
	global tag_users

	if (tag in tag_users):
		if userIP in tag_users[tag]:
			tag_users[tag].remove(userIP)  

	print (tag_users)

def resolve_rcvd_msg(message, sender=0):
	msg_parts = message.split(" ")
	rm =[]
	add =[]
	spread =[]
	for p in msg_parts:
		if p[0] == '#':
			tag = re.match("#(\w*)",p).group()
			if len(tag) > 1:
				spread.append(tag[1:])
				#add 'tag' to users preferences
		elif p[0] == '+':
			tag = re.match("\+(\w*)",p).group()
			if len(tag) > 1:
				add.append(tag[1:])
		elif p[0] == '-':
			tag = re.match("-(\w*)",p).group()
			if len(tag) > 1:
				rm.append(tag[1:])

	print("add to",sender, "=", add)
	for tg in add:
		add_tag_users(tg, sender)
		#reply confirming added tag

	print("rm from",sender,"=", rm)
	for tg in rm:
		rm_tag_users(tg, sender)
		#reply confirming removed tag

	print("spread=", spread)
	if len(spread) > 0:
		return (spread,message)
	else:
		return -1





if __name__ == "__main__":
	
	resolve_rcvd_msg(list(sys.argv)[1])
