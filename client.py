# import socket
# from concurrent.futures import ThreadPoolExecutor


# # print('connecting to %s port %s' % server_address)

# def make_req(message):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_address = ('localhost', 5001)
#     sock.connect(server_address)
#     try:
#         print('sending "%s"' % message)
#         sock.sendall(message.encode())
#         amount_received = 0
#         amount_expected = len(message)
#         while amount_received < amount_expected:
#             data = sock.recv(16)
#             amount_received += len(data)
#             print('received "%s"' % data)

#     finally:
#         print('closing socket')
#         sock.close()

# e = ThreadPoolExecutor(max_workers=13)
# # for i in range(5):
# e.submit(make_req, 'hallo')
# e.submit(make_req, 'bye')
# e.submit(make_req, 'testing')