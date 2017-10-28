import sys
import socket
import argparse
import json
from datetime import datetime

def process_args():
    parser = argparse.ArgumentParser(description='Connect to a server using TCP or UDP' +
                                     'using a pure-streaming or stop-and-wait protocol')
    parser.add_argument('host', type=str, default=socket.gethostname(),
                        help='name of the host to connect to')
    parser.add_argument('port_num', type=int, default=12397,
                        help='port number to connect to')
    parser.add_argument('protocol', type=str, default="tcp",
                        help='connect to server via tcp or udp')
    parser.add_argument('awk_type', type=str, default="streaming",
                        help='choose pure-streaming or stop-and-wait protocol')
    parser.add_argument('msg_size', type=int, default=1024,
                        help='number of bytes to send to receive')

    args = parser.parse_args()
    args.protocol = verify_input(args.protocol, "tcp", "udp")
    args.awk_type = verify_input(args.awk_type, "pure-streaming", "stop-and-wait")

    return args


# method used to verify user input is either 1 of 2 options
def verify_input(given, option1, option2):
    while given != option1 and given != option2:
        given = raw_input("Please enter in either " +
                            str(option1) +
                            " or " +
                            str(option2) +
                            ": ").lower()
    return given


# method to connect to socket and send initial message to server
def connect_sock(args):
    if args.protocol == "tcp":
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock.connect((args.host, args.port_num))

    msg = {'awk_protocol': args.awk_type, 'total_size': 2**30, 'msg_size': args.msg_size}
    print "Sending info to server"
    client_sock.send(json.dumps(msg))
    if args.protocol == "tcp":
        client_sock.recv(1)
    print "Received response from server"

    return client_sock


def send_bytes(args, client_sock):
    print "Preparing to send bytes of size " + str(args.msg_size) + " ..."
    count = 2000
    buff = bytearray(args.msg_size)
    while (count > 0):
        print "Sending bytes of size " + str(args.msg_size) + " ..."
        bytes_sent = client_sock.send(buff)
        if bytes_sent != args.msg_size:
            return
        count -= bytes_sent
        print count
        if args.awk_type == "stop-and-wait":
            print "stopandwait"
            ack = client_sock.recv(1)


def main():
    args = process_args()

    client_sock = connect_sock(args)
    start = datetime.now()

    send_bytes(args, client_sock)

    end = datetime.now()
    delta = (end - start)/2**20

    client_sock.close()


if __name__ == "__main__":
    main()
