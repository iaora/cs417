import sys
import socket
import argparse
import json

def process_args():
    parser = argparse.ArgumentParser(description='Connect to a server using TCP or UDP' +
                                     'using a streaming or stop-and-wait protocol')
    parser.add_argument('host', type=str, default=socket.gethostname(),
                        help='name of the host to connect to')
    parser.add_argument('port_num', type=int, default=12397,
                        help='port number to connect to')
    parser.add_argument('protocol', type=str, default="tcp",
                        help='connect to server via tcp or udp')
    parser.add_argument('awk_type', type=str, default="streaming",
                        help='choose streaming or stop-and-wait protocol')
    parser.add_argument('msg_size', type=int, default=1024,
                        help='number of bytes to send to receive')

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
    client_sock.connect((args.host, args.port_num))

    msg = {'protocol': args.protocol, 'total_size': args.msg_size}
    client_sock.send(json.dumps(msg))

    return client_sock


def pure_streaming():
    return


def stop_and_wait():
    return


def main():
    args = process_args()

    client_sock = connect_sock(args)

    client_sock.close()


if __name__ == "__main__":
    main()
