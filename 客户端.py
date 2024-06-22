import socket
def main():
    server_ip = '192.168.246.213'
    server_port = 79

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((server_ip, server_port))

    while True:
        message = input("请输入要发送的消息 (输入 'exit' 退出)：")
        if message == 'exit':
            break

        client_socket.send(message.encode())

    client_socket.close()

if __name__ == '__main__':
    main()