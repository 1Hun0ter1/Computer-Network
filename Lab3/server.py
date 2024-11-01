import socket
import threading
import os
import argparse
import mimetypes  # 用于设置正确的 Content-Type

is_running = True  # 全局标志变量

def handleRequest(tcpSocket):
    try:
        # 1. 接收客户端请求
        request = tcpSocket.recv(1024).decode()

        # 2. 提取请求的文件路径
        request_line = request.splitlines()[0]
        file_path = request_line.split()[1]

        if file_path == '/':
            file_path = '/index.html'  # 默认文件

        try:
            # 3. 打开文件并读取内容
            with open(file_path[1:], 'rb') as file:  # 去掉前面的 '/'
                response_body = file.read()

            # 确定 Content-Type
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'

            # 4. 构造HTTP响应头
            response_header = 'HTTP/1.1 200 OK\r\n'
            response_header += f'Content-Type: {mime_type}\r\n'
            response_header += f'Content-Length: {len(response_body)}\r\n'
            response_header += 'Connection: close\r\n\r\n'
        except FileNotFoundError:
            # 文件不存在，返回404错误
            response_header = 'HTTP/1.1 404 Not Found\r\n\r\n'
            response_body = b"<html><body><h1>404 Not Found</h1></body></html>"

        # 5. 发送响应头和内容
        tcpSocket.sendall(response_header.encode() + response_body)
    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        # 6. 关闭连接
        tcpSocket.close()


def startServer(serverAddress, serverPort):
    global is_running

    # 创建服务器套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((serverAddress, serverPort))
    server_socket.listen(5)
    print(f"Server listening on {serverAddress}:{serverPort}")

    try:
        while is_running:
            # 设置超时，以便定期检查 is_running 状态
            server_socket.settimeout(1.0)
            try:
                client_socket, client_address = server_socket.accept()
                print(f"Connection from {client_address}")
                thread = threading.Thread(target=handleRequest, args=(client_socket,))
                thread.start()
            except socket.timeout:
                continue  # 在超时时继续检查 is_running
    finally:
        server_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple HTTP Web Server")
    parser.add_argument('--host', default='127.0.0.1', help='Server IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8080, help='Server port (default: 8080)')

    args = parser.parse_args()

    # startServer(args.host, args.port)

    try:
        startServer(args.host, args.port)
    except KeyboardInterrupt:
        is_running = False  # 设置标志为 False 以停止服务器

# python server.py --port 8080