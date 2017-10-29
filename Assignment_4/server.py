import sys
import socket
import argparse
import json

def process_args():
    parser = argparse.ArgumentParser(description='Connect to a client using TCP or UDP' +
                                     'using a pure streaming or stop-and-wait protocol')
    parser.add_argument('port_num', type=int,
                        help='port number to connect to')
    parser.add_argument('protocol', type=str,
                        help='connect to server via tcp or udp')
    #parser.add_argument('awk_type', type=str, default="streaming",
    #                    help='choose pure-streaming or stop-and-wait protocol')

    args = parser.parse_args()
    args.protocol = verify_input(args.protocol, "tcp", "udp")
    #args.awk_type = verify_input(args.awk_type, "pure-streaming", "stop-and-wait")

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
        server_sock = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)
    else:
        server_sock = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
    server_sock.bind(('', args.port_num))

    return server_sock

# method to handle all TCP transfers
def receive_bytes_tcp(args, ini_data, conn):
    print "Receiving bytes.."

    count = 0
    msg_count = 0
    bytes_read = conn.recv(ini_data['msg_size'])

    # Continue looping while still data being read
    while (len(bytes_read) != 0):
        if ini_data['awk_protocol'] == "stop-and-wait":
            conn.send(bytearray(1))
        count += len(bytes_read)
        bytes_read = conn.recv(ini_data['msg_size'])
        if count >= ini_data['total_size']:
            break
        msg_count += 1
    return count, msg_count


# Method to handle all TCP connections
def tcp(server_sock, args):
    server_sock.listen(1)
    while True:
        print "Waiting for connection.."

        # Set timeout for a client connecting to server
        server_sock.settimeout(10)
        try:
            conn, addr = server_sock.accept()
        except socket.timeout:
            print "Socket timed out.. closing socket."
            break

        # Handle client sending data to server
        print "Connected by" + str(addr)
        try:
            ini_data = json.loads(conn.recv(100))
            conn.send(bytearray(1))
            bytes_received, msg_count = receive_bytes_tcp(args,
                                                ini_data,
                                                conn=conn)
            print "Number of bytes received: " + str(bytes_received)
            print "Number of messages received: " + str(msg_count)
            print "Ack protocol used: " + ini_data['awk_protocol']
        finally:
            print "Closing connection.."
            conn.close()


# Method to handle all UDP connections
def udp(server_sock, args):
    # Get initial data
    ini_data = server_sock.recvfrom(1024)
    ini_data = json.loads(ini_data[0])

    # Handle receiving bytes from client in UDP
    bytes_received, msg_count = receive_bytes_udp(args,
                                        ini_data,
                                        server_sock=server_sock)
    print "Number of bytes received: " + str(bytes_received)
    print "Number of messages received: " + str(msg_count)
    print "Ack protocol used: " + ini_data['awk_protocol']


# method to handle all UDP transfers
def receive_bytes_udp(args, ini_data, server_sock):
    print "Receiving bytes ..."

    count = 0
    bytes_read, addr = server_sock.recvfrom(ini_data['msg_size'])
    server_sock.settimeout(5)
    msg_count = 0
    while (bytes_read):
        count += len(bytes_read)
        if ini_data['awk_protocol'] == "stop-and-wait":
            server_sock.sendto(bytearray(1), addr)
        try:
            bytes_read, addr = server_sock.recvfrom(ini_data['msg_size'])
        except socket.timeout:
            print "Socket timed out.. closing socket"
            break
        if count >= ini_data['total_size']:
            break
        msg_count += 1
    return count, msg_count


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
