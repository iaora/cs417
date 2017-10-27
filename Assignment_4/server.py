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
    if args.protocol == "tcp":
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock.bind(('', args.port_num))

    return client_sock


def receive_bytes(args, conn, ini_data):
    print "Receiving bytes ..."
    count = 0
    bytes_read = conn.recv(args.msg_size)
    print sys.getsizeof(bytes_read)

    while (bytes_read != 0):
        print sys.getsizeof(bytes_read)
        bytes_read = conn.recv(args.msg_size)
    #    try:
    #        count += bytes_read
    #        if ini_data['awk_protocol'] == "stop-and-wait":
    #            send(ackbuf, 1)
    #        if count >= ini_data['total_size']:
    #            break
    #    except socket.error:
    #        print "Error"
    #        break


def main():
    args = process_args()

    client_sock = connect_sock(args)
    print "Listening on port " + str(args.port_num)

    client_sock.listen(1)

    while True:
        print "Waiting for connection..."
        conn, addr = client_sock.accept()
        print "Connected by" + str(addr)
        try:
            ini_data = json.loads(conn.recv(1))
            #receive_bytes(args, conn, ini_data)
        finally:
            print "lol"
        #    conn.close()

    client_sock.close()

if __name__ == "__main__":
    main()
