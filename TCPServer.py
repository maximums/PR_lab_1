import socket
import time
from concurrent.futures import ThreadPoolExecutor


def server(addr, port, data_list):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((addr, port))
    sock.listen()
    print('Waiting for a connection')
    with ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            connection, client_address = sock.accept()
            executor.submit(handler, connection, client_address, data_list)
    return

def handler(connection, client_address, data_list):
    try:
        print('Connection: ', client_address)
        connection.sendall("\rType 'selectColumn column_name/all or selectFromColumn column_name glob_pattern\r\n".encode())
        while True:
            data = connection.recv(1024)
            if not data:
                break
            data = data.decode()
            query_req(data, data_list, connection)
    finally:
        connection.close()
    return

def query_req(data, data_list, connection):
    data_words = data.split(' ')
    if data_words[0] == 'selectColumn':
        if data_words[1] == 'all':
            for dic in data_list:
                for item in dic.items():
                    connection.sendall((str(item)+'\n\r').encode())
            return
        for dic in data_list:
            for item in dic.items():
                if data_words[1] == item[0]:
                    connection.sendall((str(item)+'\n\r').encode())
    elif data_words[0] == 'selectFromColumn':
        for dic in data_list:
            for item in dic.items():
                if data_words[1] == item[0] and data_words[2] == item[1]:
                    connection.sendall((str(dic)+'\n\r').encode())
    else:
        connection.sendall("\n\rInvalid input\n\rTry 'selectColumn column_name/all or selectFromColumn column_name glob_pattern\r\n".encode())
    return
            

