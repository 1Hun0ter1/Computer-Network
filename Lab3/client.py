import socket
import argparse
import threading
import concurrent.futures
import time


# 定义发送请求的函数
def send_request(serverAddress, serverPort, file_path):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((serverAddress, serverPort))

            # 构造 HTTP GET 请求
            request = f"GET {file_path} HTTP/1.1\r\nHost: {serverAddress}\r\nConnection: close\r\n\r\n"
            client_socket.sendall(request.encode())

            # 接收服务器响应
            response = b""
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                response += data

            print(f"Response from server:\n{response.decode()}\n")
    except Exception as e:
        print(f"Error: {e}")

# 定义模拟多客户端请求的函数
def simulate_multiple_clients(serverAddress, serverPort, file_path, num_clients):
    threads = []
    for _ in range(num_clients):
        thread = threading.Thread(target=send_request, args=(serverAddress, serverPort, file_path))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple HTTP Client for Load Testing")
    parser.add_argument('--host', default='127.0.0.1', help='Server IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8080, help='Server port (default: 8080)')
    parser.add_argument('--file', default='/index.html', help='File path to request (default: /index.html)')
    parser.add_argument('--clients', type=int, default=1, help='Number of concurrent clients to simulate (default: 1)')

    args = parser.parse_args()

    # 启动多客户端模拟
    print(f"Simulating {args.clients} clients connecting to {args.host}:{args.port}")
    simulate_multiple_clients(args.host, args.port, args.file, args.clients)

# python client.py --host 127.0.0.1 --port 8080 --file /index.html --clients 50