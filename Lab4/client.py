import socket
import argparse
import threading
import concurrent.futures
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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


# 启动客户端模拟的函数，用于 GUI 中的启动按钮
def start_simulation():
    serverAddress = server_ip_entry.get()
    serverPort = int(server_port_entry.get())
    file_path = file_path_entry.get()
    num_clients = int(num_clients_entry.get())

    print(f"Simulating {num_clients} clients connecting to {serverAddress}:{serverPort}")
    simulate_multiple_clients(serverAddress, serverPort, file_path, num_clients)
    messagebox.showinfo("Simulation Complete", f"{num_clients} clients have completed requests.")

# 创建 GUI
root = tk.Tk()
root.title("HTTP Client Load Simulator")

# Server IP
tk.Label(root, text="Server IP:").grid(row=0, column=0, padx=10, pady=5)
server_ip_entry = tk.Entry(root)
server_ip_entry.grid(row=0, column=1, padx=10, pady=5)
server_ip_entry.insert(0, "127.0.0.1")

# Server Port
tk.Label(root, text="Server Port:").grid(row=1, column=0, padx=10, pady=5)
server_port_entry = tk.Entry(root)
server_port_entry.grid(row=1, column=1, padx=10, pady=5)
server_port_entry.insert(0, "8080")

# File Path
tk.Label(root, text="File Path:").grid(row=2, column=0, padx=10, pady=5)
file_path_entry = tk.Entry(root)
file_path_entry.grid(row=2, column=1, padx=10, pady=5)
file_path_entry.insert(0, "/index.html")

# Number of Clients
tk.Label(root, text="Number of Clients:").grid(row=3, column=0, padx=10, pady=5)
num_clients_entry = tk.Entry(root)
num_clients_entry.grid(row=3, column=1, padx=10, pady=5)
num_clients_entry.insert(0, "1")

# Start Button
start_button = tk.Button(root, text="Start Simulation", command=start_simulation)
start_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()

#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Simple HTTP Client for Load Testing")
#     parser.add_argument('--host', default='127.0.0.1', help='Server IP address (default: 127.0.0.1)')
#     parser.add_argument('--port', type=int, default=8080, help='Server port (default: 8080)')
#     parser.add_argument('--file', default='/index.html', help='File path to request (default: /index.html)')
#     parser.add_argument('--clients', type=int, default=1, help='Number of concurrent clients to simulate (default: 1)')
#
#     args = parser.parse_args()
#
#     # 启动多客户端模拟
#     print(f"Simulating {args.clients} clients connecting to {args.host}:{args.port}")
#     simulate_multiple_clients(args.host, args.port, args.file, args.clients)

# python client.py --host 127.0.0.1 --port 8080 --file /index.html --clients 50