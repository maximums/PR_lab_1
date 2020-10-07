import socket
import time
from concurrent.futures import ThreadPoolExecutor


def server(addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((addr, port))
    sock.listen()
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(handler, sock)
        executor.submit(handler, sock)
        executor.submit(handler, sock)
        executor.submit(handler, sock)
    return

def handler(sock):
    while True:
        print('Waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('Connection: ', client_address)
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                data = data.decode()
                print(data)
                connection.sendall('new version of tcp'.encode())
        finally:
            connection.close()
    return

if __name__ == "__main__":
    server('localhost', 5001)
