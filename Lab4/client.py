import socket
import argparse
import threading
import concurrent.futures
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# 定义发送请求的函数
def send_request(proxyAddress, proxyPort, method, file_path, body=None):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((proxyAddress, proxyPort))

            # 构造 HTTP GET 请求
            request = f"{method} {file_path} HTTP/1.1\r\nHost: {proxyAddress}\r\nConnection: close\r\n\r\n"
            client_socket.sendall(request.encode())

            if body:
                request += body

            # 接收服务器响应
            response = b""
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                response += data

            response_str = response.decode()
            print(f"Response from server:\n{response.decode()}\n")
            return response_str
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

# 定义模拟多客户端请求的函数
def simulate_multiple_clients(proxyAddress, proxyPort, method, file_path, num_clients, body=None):
    threads = []
    responses = []

    def threaded_request():
        response = send_request(proxyAddress, proxyPort, method, file_path, body)
        responses.append(response)


    for _ in range(num_clients):
        thread = threading.Thread(target=threaded_request)
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("Simulation complete. All requests processed.")
    return responses


# 启动客户端模拟的函数，用于 GUI 中的启动按钮
def start_simulation():
    proxyAddress = proxy_ip_entry.get()
    proxyPort = int(proxy_port_entry.get())
    method = method_combobox.get()
    file_path = file_path_entry.get()
    num_clients = int(num_clients_entry.get())
    body = body_text.get("1.0", tk.END).strip()

    responses = simulate_multiple_clients(proxyAddress, proxyPort, method, file_path, num_clients,
                                          body if body else None)
    # Display the last response in the UI for debugging purposes
    if responses:
        response_display.delete("1.0", tk.END)
        response_display.insert(tk.END, responses[-1])

    messagebox.showinfo("Simulation Complete", f"{num_clients} clients have completed {method} requests.")
    #
    # print(f"Simulating {num_clients} clients connecting to {serverAddress}:{serverPort}")
    # simulate_multiple_clients(serverAddress, serverPort, file_path, num_clients)
    # messagebox.showinfo("Simulation Complete", f"{num_clients} clients have completed requests.")

# 创建 GUI
root = tk.Tk()
root.title("HTTP Client Load Simulator")
# Proxy IP Address
tk.Label(root, text="Proxy IP:").grid(row=0, column=0, padx=10, pady=5)
proxy_ip_entry = tk.Entry(root)
proxy_ip_entry.grid(row=0, column=1, padx=10, pady=5)
proxy_ip_entry.insert(0, "127.0.0.1")

# Proxy Port
tk.Label(root, text="Proxy Port:").grid(row=1, column=0, padx=10, pady=5)
proxy_port_entry = tk.Entry(root)
proxy_port_entry.grid(row=1, column=1, padx=10, pady=5)
proxy_port_entry.insert(0, "8000")

# HTTP Method
tk.Label(root, text="HTTP Method:").grid(row=2, column=0, padx=10, pady=5)
method_combobox = ttk.Combobox(root, values=["GET", "POST", "PUT", "DELETE"], state="readonly")
method_combobox.grid(row=2, column=1, padx=10, pady=5)
method_combobox.set("GET")

# File Path
tk.Label(root, text="File Path:").grid(row=3, column=0, padx=10, pady=5)
file_path_entry = tk.Entry(root)
file_path_entry.grid(row=3, column=1, padx=10, pady=5)
file_path_entry.insert(0, "/index.html")

# Number of Clients
tk.Label(root, text="Number of Clients:").grid(row=4, column=0, padx=10, pady=5)
num_clients_entry = tk.Entry(root)
num_clients_entry.grid(row=4, column=1, padx=10, pady=5)
num_clients_entry.insert(0, "1")

# Request Body
tk.Label(root, text="Request Body (for POST/PUT):").grid(row=5, column=0, padx=10, pady=5)
body_text = tk.Text(root, height=10, width=60)
body_text.grid(row=5, column=1, padx=10, pady=5)

# Start Button
start_button = tk.Button(root, text="Start Simulation", command=start_simulation, bg="green", fg="white")
start_button.grid(row=6, column=0, columnspan=2, pady=10)

# Response Display Area
tk.Label(root, text="Response:").grid(row=7, column=0, columnspan=2, padx=10, pady=5)
response_display = tk.Text(root, wrap=tk.WORD, width=90, height=20)
response_display.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

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