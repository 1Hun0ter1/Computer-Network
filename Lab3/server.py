import socket
import threading
import os
import logging
import argparse
import mimetypes  # 用于设置正确的 Content-Type
import time
from collections import defaultdict


is_running = True  # 全局标志变量

# 设置日志记录
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# 记录请求日志的函数
def log_request(client_address, file_path, status_code):
    logging.info(f"Client: {client_address}, File: {file_path}, Status: {status_code}")

# 速率限制的请求记录
request_times = defaultdict(list)

# 获取文件的 MIME 类型
def get_content_type(file_path):
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or 'application/octet-stream'

# 速率限制函数（限制每个 IP 每分钟请求数）
def rate_limit(client_ip, max_requests=5, window=60):
    current_time = time.time()
    request_times[client_ip] = [t for t in request_times[client_ip] if t > current_time - window]
    request_times[client_ip].append(current_time)
    return len(request_times[client_ip]) <= max_requests


def handleRequest(tcpSocket):
    try:
        # 1. 接收客户端请求
        request = tcpSocket.recv(1024).decode()

        # 2. 提取请求的文件路径
        request_line = request.splitlines()[0]
        file_path = request_line.split()[1]

        if file_path == '/':
            file_path = '/index.html'  # 默认文件

        # 获取客户端 IP 地址用于速率限制
        client_ip = tcpSocket.getpeername()[0]
        if not rate_limit(client_ip):
            tcpSocket.sendall("HTTP/1.1 429 Too Many Requests\r\n\r\n".encode())
            tcpSocket.close()
            return


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
            response_header += f'Content-Type: {get_content_type(file_path)}\r\n'
            response_header += f'Content-Length: {len(response_body)}\r\n'
            response_header += 'Connection: close\r\n\r\n'
            status_code = 200
        except FileNotFoundError:
            # 文件不存在，返回404错误
            response_header = 'HTTP/1.1 404 Not Found\r\n\r\n'
            response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
            status_code = 404

        # 5. 发送响应头和内容
        tcpSocket.sendall(response_header.encode() + response_body)

        log_request(client_ip, file_path, status_code)
    except Exception as e:
        logging.error(f"Error handling request: {e}")
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