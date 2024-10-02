#!/usr/bin/env python3

import socket
import sys
import threading

def SERVER(l_host, l_port, r_host, r_port, catch_data):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((l_host, l_port))
    except socket.error as err:
        print(f'ERROR: {str(err)}')
    server.listen(5)
    print(f'[✅] Server Listening On {l_host}:{l_port}')

    while True:
        client_socket, addr = server.accept()
        print(f'Got a connection from {addr[0]}:{addr[1]}')
        proxy_thread = threading.Thread(target=controller, args=(client_socket, r_host, r_port, catch_data))
        proxy_thread.start()

def recv_from(socket_):
    buffer = b''
    socket_.settimeout(10)
    try:
        while True:
            data = socket_.recv(1024)
            if not data:
                break
            buffer += data
    except socket.timeout:
        print('[❌] Timeout!')
    except Exception as e:
        print(f'[❌] Error: {e}')
    return buffer

def controller(client_socket, r_host, r_port, catch_data):
    r_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_socket.connect((r_host, r_port))

    if catch_data:  # Capture data from remote server first if required
        remote_buffer = recv_from(r_socket)
        if len(remote_buffer):
            print(f'[↩] Sending {len(remote_buffer)} bytes to client!')
            client_socket.send(remote_buffer)

    while True:
        local_buffer = recv_from(client_socket)
        if len(local_buffer):
            print(f'[🥇] RECEIVED {len(local_buffer)} bytes from client!')
            r_socket.send(local_buffer)
            print(f'[➡] Sent to remote!')

        remote_buffer = recv_from(r_socket)
        if len(remote_buffer):
            print(f'[🥇] RECEIVED {len(remote_buffer)} bytes from remote!')
            client_socket.send(remote_buffer)
            print(f'[⬅] Sent to client!')

        if not len(local_buffer) or not len(remote_buffer):
            r_socket.close()
            client_socket.close()
            print('[❌] No data available, terminating!')
            break

def main():
    if len(sys.argv[1:]) != 5:
        print(f"Usage: python3 {sys.argv[0]} [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print(f"Example: python3 {sys.argv[0]} 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    catch_first = sys.argv[5].lower() == 'true'

    SERVER(local_host, local_port, remote_host, remote_port, catch_first)

if __name__ == "__main__":
    main()
