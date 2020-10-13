from abc import ABCMeta, abstractstaticmethod

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
            self._conn.sendall(('\r\nCommand ' + str(command_name) + ' not recognised\r\n').encode())

class ICommand(metaclass=ABCMeta):
    @abstractstaticmethod
    def execute(args):
        pass


class Query:
    def __init__(self, data_list, connection):
        self._data_list = data_list
        self._conn = connection
        self._keys = []
        self._values = []
        for dic in self._data_list:
            self._keys.extend(dic.keys())
        for dic in self._data_list:
            self._values.extend(dic.values())
        self._keys.append('all')

    def select_column(self, args):
        if args[0] not in self._keys:
            self._conn.sendall(('\r\nUnknown column name '+args[0]).encode())
            return
        if args[0] == 'all':
            for dic in self._data_list:
                for item in dic.items():
                    self._conn.sendall((str(item)+'\n\r').encode())
        else:
            for dic in self._data_list:
                for item in dic.items():
                    if args[0] == item[0]:
                        self._conn.sendall((str(item)+'\n\r').encode())

    def select_from_column(self, args):
        if args[0] not in self._keys:
            self._conn.sendall(("\r\nUnknown column name '"+args[0]+"'").encode())
        if args[1] not in self._values:
            self._conn.sendall(("\r\nUnknown global pattern '"+args[1]+"'").encode())
            return
        for dic in self._data_list:
            for item in dic.items():
                if args[0] == item[0] and args[1] == item[1]:
                    self._conn.sendall((str(dic)+'\n\r').encode())      

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