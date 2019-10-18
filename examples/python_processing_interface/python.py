import socket

HOST = ''
PORT = 50007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))

s.listen(1)

conn, addr = s.accept()
print('Connected by', addr)

while True:
    #data = conn.recv(1024)
    #if not data:
    #    break
    #print(data)
    print("sending")
    conn.send(b"hello from python")

conn.close()