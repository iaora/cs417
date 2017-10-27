import sys
import socket
import argparse
import json

def process_args():
    parser = argparse.ArgumentParser(description='Connect to a client using TCP or UDP' +
                                     'using a streaming or stop-and-wait protocol')
    parser.add_argument('port_num', type=int, default=12397,
                        help='port number to connect to')
    parser.add_argument('protocol', type=str, default="tcp",
                        help='connect to server via tcp or udp')
    parser.add_argument('awk_type', type=str, default="streaming",
                        help='choose streaming or stop-and-wait protocol')

    args = parser.parse_args()
    args.protocol = verify_input(args.protocol, "tcp", "udp")
    args.awk_type = verify_input(args.awk_type, "streaming", "stop-and-wait")

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


def pure_streaming():
    return


def stop_and_wait():
    return


def main():
    args = process_args()

    client_sock = connect_sock(args)
    print "Listening on port " + str(args.port_num)

    client_sock.listen(1)

    print "Waiting for connection..."
    conn, addr = client_sock.accept()
    print "Connected by" + str(addr)
    try:
        data = conn.recv(2014)
        print "Client says: " + str(data)
        
    except socket.error:
        print "Error"
    finally:
        conn.close()


if __name__ == "__main__":
    main()
