import socket
import threading
import os
import logging
import mimetypes
import time
import tkinter as tk
from tkinter import scrolledtext
from collections import defaultdict
import configparser

# Global variable for server running status
is_running = True

# Read server configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Server configuration
HOST = config['server'].get('host', '127.0.0.1')
PORT = config['server'].getint('port', 8080)
MAX_CONNECTIONS = config['server'].getint('max_connections', 5)
max_requests = config['rate_limit'].getint('max_requests', 5)
window = config['rate_limit'].getint('window_seconds', 60)

# Security settings
whitelist = set(config['security']['whitelist'].split(',')) if config['security']['whitelist'] else set()
blacklist = set(config['security']['blacklist'].split(',')) if config['security']['blacklist'] else set()

# Logging setup
logging.basicConfig(level=logging.INFO)

# Rate limit tracking dictionary
request_times = defaultdict(list)

# Initialize Tkinter GUI
root = tk.Tk()
root.title("Server Dashboard")
root.geometry("400x550")

# Log display area in GUI
log_area = scrolledtext.ScrolledText(root, width=90, height=20, state='disabled', wrap='word', font=('Courier', 10))
log_area.pack(pady=10)

# Server status label
status_label = tk.Label(root, text="Server Status: Stopped", font=("Helvetica", 12, "bold"), fg="red")
status_label.pack(pady=10)

# Function to log messages to the GUI
def log_message(message, color="black"):
    log_area.config(state='normal')
    log_area.insert(tk.END, message + "\n", ("color",))
    log_area.tag_config("color", foreground=color)
    log_area.config(state='disabled')
    log_area.see(tk.END)

# Function to get content type for files
def get_content_type(file_path):
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or 'application/octet-stream'

# Rate limiting function
def rate_limit(client_ip):
    current_time = time.time()
    request_times[client_ip] = [t for t in request_times[client_ip] if t > current_time - window]
    request_times[client_ip].append(current_time)
    return len(request_times[client_ip]) <= max_requests

# Handle incoming requests
def handle_request(tcp_socket, client_address):
    client_ip = client_address[0]
    try:
        # Check blacklist and whitelist
        if client_ip in blacklist:
            tcp_socket.sendall("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
            log_message(f"Blocked {client_ip} - Blacklisted", "red")
            return
        if whitelist and client_ip not in whitelist:
            tcp_socket.sendall("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
            log_message(f"Blocked {client_ip} - Not Whitelisted", "red")
            return

        # Rate limiting check
        if not rate_limit(client_ip):
            tcp_socket.sendall("HTTP/1.1 429 Too Many Requests\r\n\r\n".encode())
            log_message(f"{client_ip} - Rate Limit Exceeded (429)", "orange")
            return

        # Receive request
        request = tcp_socket.recv(1024).decode()
        request_line = request.splitlines()[0]
        parts = request_line.split()

        if len(parts) < 3:
            tcp_socket.sendall("HTTP/1.1 400 Bad Request\r\n\r\n".encode())
            log_message(f"{client_ip} - Invalid Request Format (400)", "purple")
            return

        method = parts[0]
        file_path = parts[1]
        if file_path == '/':
            file_path = '/index.html'

        # Path traversal prevention
        if ".." in file_path or file_path.startswith("/.."):
            tcp_socket.sendall("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
            log_message(f"{client_ip} - Path Traversal Attempt Blocked (403)", "red")
            return

        # Read the body for methods like POST, PUT
        body = None
        # if "Content-Length" in request:
        #     content_length = int([line.split(": ")[1] for line in request.splitlines() if "Content-Length" in line][0])
        #     body = tcp_socket.recv(content_length).decode()
        if "Content-Length" in request:
            content_length = int([line.split(": ")[1] for line in request.splitlines() if "Content-Length" in line][0])

            headers_end = request.find("\r\n\r\n") + 4  # 找到空行结束的位置
            body_start = headers_end
            body = request[body_start:body_start + content_length]

        # Handle HTTP methods
        if method == "GET":
            try:
                with open(file_path[1:], 'rb') as file:
                    response_body = file.read()
                content_type = get_content_type(file_path)
                response_header = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(response_body)}\r\nConnection: close\r\n\r\n"
                tcp_socket.sendall(response_header.encode() + response_body)
                log_message(f"{client_ip} - File Served: {file_path} (200)", "green")
            except FileNotFoundError:
                tcp_socket.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                log_message(f"{client_ip} - File Not Found (404)", "orange")

        elif method == "POST":
            try:
                with open(file_path[1:], "a") as file:
                    print(body)
                    file.write(body or "")
                tcp_socket.sendall("HTTP/1.1 200 OK\r\n\r\nData Appended Successfully".encode())
                log_message(f"{client_ip} - POST: Data Appended to {file_path} (200)", "green")
            except FileNotFoundError:
                with open(file_path[1:], "w") as file:
                    file.write(body or "")
                tcp_socket.sendall("HTTP/1.1 201 Created\r\n\r\nFile Created and Data Appended".encode())
                log_message(f"{client_ip} - POST: File Created and Data Appended to {file_path} (201)", "blue")

        elif method == "PUT":
            try:
                with open(file_path[1:], "w") as file:
                    file.write(body or "")
                tcp_socket.sendall("HTTP/1.1 201 Created\r\n\r\nFile Created Successfully".encode())
                log_message(f"{client_ip} - PUT: File {file_path} Created (201)", "green")
            except Exception as e:
                tcp_socket.sendall(f"HTTP/1.1 500 Internal Server Error\r\n\r\n{e}".encode())
                log_message(f"{client_ip} - PUT Error: {e} (500)", "red")

        elif method == "DELETE":
            try:
                os.remove(file_path[1:])
                tcp_socket.sendall("HTTP/1.1 200 OK\r\n\r\nFile Deleted Successfully".encode())
                log_message(f"{client_ip} - DELETE: File {file_path} Deleted (200)", "green")
            except FileNotFoundError:
                tcp_socket.sendall("HTTP/1.1 404 Not Found\r\n\r\nFile Not Found".encode())
                log_message(f"{client_ip} - DELETE: File Not Found (404)", "orange")
            except Exception as e:
                tcp_socket.sendall(f"HTTP/1.1 500 Internal Server Error\r\n\r\n{e}".encode())
                log_message(f"{client_ip} - DELETE Error: {e} (500)", "red")

        else:
            tcp_socket.sendall(f"HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod {method} Not Allowed".encode())
            log_message(f"{client_ip} - Unsupported Method {method} (405)", "orange")

    except Exception as e:
        tcp_socket.sendall("HTTP/1.1 500 Internal Server Error\r\n\r\n".encode())
        log_message(f"Error handling request from {client_address}: {e}", "red")
    finally:
        tcp_socket.close()

# Server startup function
def start_server():
    global is_running
    status_label.config(text="Server Status: Running", fg="green")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse socket
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)
    log_message(f"Server started on {HOST}:{PORT}", "blue")

    try:
        while is_running:
            server_socket.settimeout(1.0)
            try:
                client_socket, client_address = server_socket.accept()
                threading.Thread(target=handle_request, args=(client_socket, client_address)).start()
            except socket.timeout:
                continue
    finally:
        server_socket.close()
        log_message("Server stopped", "blue")

# Start and stop server control functions
def start_server_thread():
    global is_running
    is_running = True
    threading.Thread(target=start_server, daemon=True).start()

def stop_server():
    global is_running
    is_running = False
    status_label.config(text="Server Status: Stopped", fg="red")
    log_message("Server stopping...", "red")

# Graceful shutdown on GUI close
def on_close():
    stop_server()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# Buttons to start and stop the server
start_button = tk.Button(root, text="Start Server", command=start_server_thread, bg="green", fg="white")
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Server", command=stop_server, bg="red", fg="white")
stop_button.pack(pady=5)

# Run the GUI main loop
root.mainloop()
