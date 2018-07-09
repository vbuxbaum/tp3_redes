#!/usr/bin/python3

import socket
import ast
import sys
import struct
import codecs
import re

tag_users = {}
args = list(sys.argv)

###############################################################################
#UDP Socket
udp_sock = socket.socket(socket.AF_INET,    # Internet
                         socket.SOCK_DGRAM)     # UDP
# bind this port on local IP to UDP socket
udp_sock.bind(("127.0.0.1", int(args[1])))

###############################################################################

def send_message_to(message,destination):
    destination = destination.split('/')
    destination[1] = int(destination[1])
    udp_sock.sendto(str.encode(message), tuple(destination))

###############################################################################

def add_tag_users(tag, userID):
    global tag_users

    if (tag in tag_users):
        if userID not in tag_users[tag]:
            tag_users[tag].append(userID)
            send_message_to("Confirmado interesse no tópico " + tag + ".", userID)
 
    else:
        tag_users[tag] = [userID]
        send_message_to("Confirmado interesse no tópico " + tag + ".", userID)


    #print (tag_users)
###############################################################################

def rm_tag_users(tag, userID):
    global tag_users

    if (tag in tag_users):
        if userID in tag_users[tag]:
            tag_users[tag].remove(userID)
            send_message_to("Removido interesse no tópico " + tag + ".", userID)
  

    #print (tag_users)
###############################################################################

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

    for tg in add:
        add_tag_users(tg, sender)
    for tg in rm:
        rm_tag_users(tg, sender)

    if len(spread) > 0:
        spread_message(spread,message)
    else:
        return -1
###############################################################################

def spread_message(tags,message):
    ids = []
    for tag in tags:
        try:
            for userID in tag_users[tag]:
                if userID not in ids:
                    send_message_to(message, userID)
                    ids.append(userID)
        except:
            continue


if __name__ == "__main__":
    while(True):
        message, addr = udp_sock.recvfrom(1024) #message is a string representation of JSON message
        message = message.decode()
        resolve_rcvd_msg(message, "/".join([str(i) for i in addr]))