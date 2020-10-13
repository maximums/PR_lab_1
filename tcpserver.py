import socket
from command_pattern import *
from concurrent.futures import ThreadPoolExecutor

BUFSIZE = 1024

def server(addr, port, data_list):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((addr, port))
    sock.listen()
    print('Waiting for a connection')
    with ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            connection, client_address = sock.accept()
            executor.submit(handler, connection, client_address, data_list)

def handler(connection, client_address, data_list):
    try:
        print('Connection: ', client_address)
        connection.sendall("\rPress Ctrl + ^]".encode())
        connection.sendall(" and type  'sen selectColumn column_name/all' or 'sen selectFromColumn column_name glob_pattern'\r\n".encode())
        while True:
            data = connection.recv(BUFSIZE)
            if not data:
                break
            req_server(data, data_list, connection)
    finally:
        connection.close()

def req_server(data, data_list, connection):
    data = data.decode()
    data = data.split(' ')
    command_name = data.pop(0)
    QUERY = Query(data_list, connection)
    SELECT_COLUMN = SelectColumn(QUERY)
    SELECT_FROM_COLUMN = SelectFromColumn(QUERY)
    INVOKER = Invoker(connection)
    INVOKER.register("selectColumn", SELECT_COLUMN)
    INVOKER.register("selectFromColumn", SELECT_FROM_COLUMN)
    INVOKER.execute(command_name, data)