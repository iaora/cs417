import sys
import socket
import argparse
import json

def process_args():
    parser = argparse.ArgumentParser(description='Connect to a client using TCP or UDP' +
                                     'using a pure streaming or stop-and-wait protocol')
    parser.add_argument('port_num', type=int, default=12397,
                        help='port number to connect to')
    parser.add_argument('protocol', type=str, default="tcp",
                        help='connect to server via tcp or udp')
    parser.add_argument('awk_type', type=str, default="streaming",
                        help='choose pure-streaming or stop-and-wait protocol')

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
    print "Listening on port " + str(args.port_num)
    if args.protocol == "tcp":
        print "tcp"
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        print "udp"
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind(('', args.port_num))

    return server_sock

# method to handle all TCP transfers
def receive_bytes_tcp(args, ini_data, conn):
    print "Receiving bytes ..."

    count = 0
    bytes_read = conn.recv(ini_data['msg_size'])
    print len(bytes_read)
    while (len(bytes_read) != 0):
        count += len(bytes_read)
        bytes_read = conn.recv(ini_data['msg_size'])
        if ini_data['awk_protocol'] == "stop-and-wait":
            send(ackbuf, 1)
        if count >= ini_data['total_size']:
            break
    print "Count: " + str(count)


# method to handle all UDP transfers
def receive_bytes_udp(args, ini_data, server_sock):
    print "Receiving bytes ..."

    count = 0
    bytes_read = server_sock.recvfrom(ini_data['msg_size'])
    server_sock.settimeout(1)
    print len(bytes_read[0])
    while (bytes_read[0]):
        count += len(bytes_read[0])
        try:
            bytes_read = server_sock.recvfrom(ini_data['msg_size'])
        except socket.timeout:
            break
        print len(bytes_read[0])
        if ini_data['awk_protocol'] == "stop-and-wait":
            send(ackbuf, 1)
        if count >= ini_data['total_size']:
            break
    print "Count: " + str(count)


# Method to handle all TCP connections
def tcp(server_sock, args):
    server_sock.listen(1)
    while True:
        print "Waiting for connection..."
        conn, addr = server_sock.accept()
        print "Connected by" + str(addr)
        try:
            ini_data = json.loads(conn.recv(100))
            conn.send(bytearray(1))
            receive_bytes_tcp(args, ini_data, conn=conn)
            conn.close()
        finally:
            print "lol"

def udp(server_sock, args):
    # Get initial data
    ini_data = server_sock.recvfrom(1024)
    ini_data = json.loads(ini_data[0])

    receive_bytes_udp(args, ini_data, server_sock=server_sock)

def main():
    args = process_args()

    server_sock = connect_sock(args)

    if args.protocol == "tcp":
        tcp(server_sock, args)
    else:
        udp(server_sock, args)

    server_sock.close()

if __name__ == "__main__":
    main()
