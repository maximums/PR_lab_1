import time
import socket
from abc import ABCMeta, abstractstaticmethod
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
        connection.sendall("\rType 'selectColumn column_name/all or selectFromColumn column_name glob_pattern\r\n".encode())
        while True:
            data = connection.recv(BUFSIZE)
            if not data:
                break
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
            print(command_name)
            print(data)
            # INVOKER.execute("selectFromColumn", 'id','3')
            # req_server(data, data_list, connection)
    finally:
        connection.close()

# def req_server(data, data_list, connection):
#     data_words = data.split(' ')
#     if data_words[0] == 'selectColumn':
#         if data_words[1] == 'all':
#             for dic in data_list:
#                 for item in dic.items():
#                     connection.sendall((str(item)+'\n\r').encode())
#         else:
#             for dic in data_list:
#                 for item in dic.items():
#                     if data_words[1] == item[0]:
#                         connection.sendall((str(item)+'\n\r').encode())
#     elif data_words[0] == 'selectFromColumn':
#         for dic in data_list:
#             for item in dic.items():
#                 if data_words[1] == item[0] and data_words[2] == item[1]:
#                     connection.sendall((str(dic)+'\n\r').encode())
#     else:
#         connection.sendall("\n\rInvalid input\n\rTry 'selectColumn column_name/all or selectFromColumn column_name glob_pattern\r\n".encode())

class Invoker:
    def __init__(self, connection):
        self._commands = {}
        self._conn = connection

    def register(self, command_name, command):
        self._commands[command_name] = command

    def execute(self, command_name, args):
        if command_name in self._commands.keys():
            self._commands[command_name].execute(args)
        else:
            self._conn.sendall('\r\nCommand ' + command_name + ' not recognised')

class ICommand(metaclass=ABCMeta):
    @abstractstaticmethod
    def execute(args):
        'Abstract method'

class Query:
    def __init__(self, data_list, connection):
        self._data_list = data_list
        self._conn = connection

    def select_column(self, args):
        # if args[0] not in self._data_list.keys():
        #     self._conn.sendall(('\n\rUnknown column name '+args[0]).encode())
        #     return
        if args[0] == 'all':
            for dic in self._data_list:
                for item in dic.items():
                    self._conn.sendall((str(item)+'\n\r').encode())
        else:
            for dic in self._data_list:
                for item in dic.items():
                    if args[0] == item[0]:
                        self._conn.sendall((str(item)+'\n\r').encode())
        print(args)

    def select_from_column(self, args):
        # if args[0] not in self._data_list.keys() and args[1] not in self._data_list.values():
        #     self._conn.sendall(('\n\rUnknown column name '+args[0]+' or global pattern '+ args[1]).encode())
        #     return
        for dic in self._data_list:
            for item in dic.items():
                if args[0] == item[0] and args[1] == item[1]:
                    self._conn.sendall((str(dic)+'\n\r').encode())
        print(args)        

class SelectColumn(ICommand):
    def __init__(self, query):
        self._query = query

    def execute(self, args):
        self._query.select_column(args)

class SelectFromColumn(ICommand):
    def __init__(self, query):
        self._query = query

    def execute(self, args):
        self._query.select_from_column(args)
          
# server('localhost', 5001, [{'asda':'adad','id':'3','email':'cdodi907'}])
