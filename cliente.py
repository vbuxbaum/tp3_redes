#!/usr/bin/python3
import socket
import sys
import select

args = list(sys.argv)   

###############################################################################
#UDP Socket
udp_sock = socket.socket(socket.AF_INET,    # Internet
                         socket.SOCK_DGRAM)     # UDP
udp_sock.settimeout(1)
# bind this port on local IP to UDP socket
udp_sock.bind(("127.0.0.1", int(args[1])))

if __name__ == "__main__":
    while(True):
        socket_list = [sys.stdin, udp_sock]
        # Get the list sockets which are readable
        print("Compartilhe aqui o que está pensando (não inclua caracteres com acentuação):")
        inputs,outputs,in_error = select.select(socket_list , [], [])
        for s in socket_list:
            if s == udp_sock:
                # incoming message from remote server
                sys.stdout.write("\n<Carregando novas mensagens...>\n\n")
                while (True):
                    try:
                        rcv_message, addr = udp_sock.recvfrom(1024) #message is a string representation of JSON message
                        message = rcv_message.decode()
                        sys.stdout.write('<Mensagem Recebida> ')
                        sys.stdout.write(message + "\n")
                        sys.stdout.flush()
                    except:
                        break
                        #continue
            else :
                # user entered a message
                message = sys.stdin.readline()
                sys.stdout.flush()
                udp_sock.sendto(str.encode(message), (args[2],int(args[3])))
