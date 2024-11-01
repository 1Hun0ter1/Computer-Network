import socket
import argparse


def send_request(serverAddress, serverPort, file_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((serverAddress, serverPort))

        # 构造HTTP GET请求
        request = f"GET {file_path} HTTP/1.1\r\nHost: {serverAddress}\r\nConnection: close\r\n\r\n"
        client_socket.sendall(request.encode())

        # 接收服务器响应
        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        print(response.decode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple HTTP Client")
    parser.add_argument('--host', default='127.0.0.1', help='Server IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8080, help='Server port (default: 8080)')
    parser.add_argument('--file', default='/index.html', help='File path to request (default: /index.html)')

    args = parser.parse_args()
    send_request(args.host, args.port, args.file)
