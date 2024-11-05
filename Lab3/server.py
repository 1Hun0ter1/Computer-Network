import socket
import threading
import os
import logging
import argparse
import mimetypes  # 用于设置正确的 Content-Type
import time
from collections import defaultdict
import configparser

is_running = True  # 全局标志变量

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')


# 服务器配置信息
HOST = config['server'].get('host', '127.0.0.1')
PORT = config['server'].getint('port', 8080)
MAX_CONNECTIONS = config['server'].getint('max_connections', 5)
max_requests = config['rate_limit'].getint('max_requests', 5)
window = config['rate_limit'].getint('window_seconds', 60)



# 安全设置
whitelist = set(config['security']['whitelist'].split(','))
blacklist = set(config['security']['blacklist'].split(','))


# 设置日志记录
log_level = config['logging'].get('level', 'INFO')
logging.basicConfig(level=getattr(logging, log_level))
# 速率限制的请求记录
request_times = defaultdict(list)

# 记录请求日志的函数
def log_request(client_address, file_path, status_code):
    logging.info(f"Client: {client_address}, File: {file_path}, Status: {status_code}")


# 获取文件的 MIME 类型
def get_content_type(file_path):
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or 'application/octet-stream'

# 速率限制函数（限制每个 IP 每分钟请求数）
def rate_limit(client_ip):
    current_time = time.time()
    request_times[client_ip] = [t for t in request_times[client_ip] if t > current_time - window]
    request_times[client_ip].append(current_time)
    return len(request_times[client_ip]) <= max_requests


def handleRequest(tcpSocket, client_address):
    client_ip = client_address[0]

    # Check blacklist and whitelist
    if client_ip in blacklist:
        tcpSocket.sendall("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
        tcpSocket.close()
        return
    if whitelist and client_ip not in whitelist:
        tcpSocket.sendall("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
        tcpSocket.close()
        return

    # Rate limiting check
    if not rate_limit(client_ip):
        tcpSocket.sendall("HTTP/1.1 429 Too Many Requests\r\n\r\n".encode())
        tcpSocket.close()
        return

    try:
        # Receive client request
        request = tcpSocket.recv(1024).decode()

        # Validate the HTTP request format
        request_line = request.splitlines()[0]
        parts = request_line.split()
        if len(parts) != 3 or parts[0] != "GET":
            # Invalid request format
            tcpSocket.sendall("HTTP/1.1 400 Bad Request\r\n\r\n".encode())
            log_request(client_ip, "INVALID REQUEST", 400)
            tcpSocket.close()
            return

        file_path = parts[1]
        if file_path == '/':
            file_path = '/index.html'  # Default file

        # Path traversal prevention
        if ".." in file_path or file_path.startswith("/.."):
            tcpSocket.sendall("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
            log_request(client_ip, file_path, 403)
            tcpSocket.close()
            return

        # Attempt to open the requested file
        try:
            with open(file_path[1:], 'rb') as file:  # Remove leading '/'
                response_body = file.read()

            # Check file permissions
            if not os.access(file_path[1:], os.R_OK):
                tcpSocket.sendall("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
                log_request(client_ip, file_path, 403)
                tcpSocket.close()
                return

            # Determine Content-Type and set UTF-8 encoding for text content
            content_type = get_content_type(file_path)
            if content_type.startswith("text/"):
                content_type += "; charset=utf-8"

            # 4. Build HTTP response headers
            response_header = 'HTTP/1.1 200 OK\r\n'
            response_header += f'Content-Type: {content_type}\r\n'
            response_header += f'Content-Length: {len(response_body)}\r\n'
            response_header += 'Connection: close\r\n\r\n'
            status_code = 200

        except FileNotFoundError:
            # File not found, return 404 error
            response_header = 'HTTP/1.1 404 Not Found\r\n\r\n'
            response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
            status_code = 404

        except PermissionError:
            # Permission denied, return 403 error
            response_header = 'HTTP/1.1 403 Forbidden\r\n\r\n'
            response_body = b"<html><body><h1>403 Forbidden</h1></body></html>"
            status_code = 403

        # Send response header and body
        tcpSocket.sendall(response_header.encode() + response_body)
        log_request(client_ip, file_path, status_code)

    except Exception as e:
        logging.error(f"Error handling request: {e}")
        tcpSocket.sendall("HTTP/1.1 500 Internal Server Error\r\n\r\n".encode())
    finally:
        tcpSocket.close()



# def startServer(serverAddress, serverPort):
def startServer():
    global is_running

    # 创建服务器套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.bind((serverAddress, serverPort))
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)
    print(f"Server listening on {HOST}:{PORT}")

    try:
        while is_running:
            # 设置超时，以便定期检查 is_running 状态
            server_socket.settimeout(1.0)
            try:
                client_socket, client_address = server_socket.accept()
                print(f"Connection from {client_address}")
                thread = threading.Thread(target=handleRequest, args=(client_socket, client_address))
                thread.start()
            except socket.timeout:
                continue  # 在超时时继续检查 is_running

    finally:
        server_socket.close()


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Simple HTTP Web Server")
    # parser.add_argument('--host', default='127.0.0.1', help='Server IP address (default: 127.0.0.1)')
    # parser.add_argument('--port', type=int, default=8080, help='Server port (default: 8080)')
    #
    # args = parser.parse_args()
    #
    # # startServer(args.host, args.port)
    #
    try:
        startServer()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        is_running = False  # 设置标志为 False 以停止服务器


# python server.py --port 8080 (旧)
# python server.py (now)