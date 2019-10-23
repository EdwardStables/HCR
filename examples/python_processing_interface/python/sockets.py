import socket
import time

class connecter:

    def __init__(self):
        HOST = ''
        PORT = 50007
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, PORT))
        self.s.listen(1)

        self.conn, self.addr = self.s.accept()
        print('Connected by', self.addr)

    def send(self, send_string):
        self.conn.send(bytes(send_string, encoding='utf-8'))

    def closer(self):
        self.conn.close()
