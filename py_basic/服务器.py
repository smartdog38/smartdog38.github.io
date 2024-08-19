from socket import socket,AF_INET,SOCK_STREAM


listen_socket = socket(AF_INET,SOCK_STREAM)
listen_socket.bind(('',8887))
listen_socket.listen(1)
isON = False
while True:
    session_socket,addr=listen_socket.accept()
    isON = True
    while isON:
        data = session_socket.recv(1024).decode('utf-8')
        print(data)
        if not data:
            isON =False
            session_socket.close()


