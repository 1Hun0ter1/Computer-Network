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
whitelist = set(config['security']['whitelist'].split(','))
blacklist = set(config['security']['blacklist'].split(','))

# Logging setup
logging.basicConfig(level=logging.INFO)

# Rate limit tracking dictionary
request_times = defaultdict(list)

# Initialize Tkinter GUI
root = tk.Tk()
root.title("Server Dashboard")
root.geometry("800x500")

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

# Request handling function
def handle_request(tcp_socket, client_address):
    client_ip = client_address[0]
    try:
        # Check blacklist and whitelist
        if client_ip in blacklist:
            tcp_socket.sendall("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
            log_message(f"Blocked {client_ip} - Blacklisted", "red")
            tcp_socket.close()
            return
        if whitelist and client_ip not in whitelist:
            tcp_socket.sendall("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
            log_message(f"Blocked {client_ip} - Not Whitelisted", "red")
            tcp_socket.close()
            return

        # Rate limiting check
        if not rate_limit(client_ip):
            tcp_socket.sendall("HTTP/1.1 429 Too Many Requests\r\n\r\n".encode())
            log_message(f"{client_ip} - Rate Limit Exceeded (429)", "orange")
            tcp_socket.close()
            return

        # Receive and process the request
        request = tcp_socket.recv(1024).decode()
        request_line = request.splitlines()[0]
        parts = request_line.split()

        # Validate request format
        if len(parts) != 3 or parts[0] != "GET":
            tcp_socket.sendall("HTTP/1.1 400 Bad Request\r\n\r\n".encode())
            log_message(f"{client_ip} - Invalid Request (400)", "purple")
            tcp_socket.close()
            return

        file_path = parts[1]
        if file_path == '/':
            file_path = '/index.html'  # Default file

        # Path traversal prevention
        if ".." in file_path or file_path.startswith("/.."):
            tcp_socket.sendall("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
            log_message(f"{client_ip} - Path Traversal Attempt Blocked (403)", "red")
            tcp_socket.close()
            return

        # Attempt to open the requested file
        try:
            with open(file_path[1:], 'rb') as file:
                response_body = file.read()

            # Check file permissions
            if not os.access(file_path[1:], os.R_OK):
                tcp_socket.sendall("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
                log_message(f"{client_ip} - Permission Denied (403)", "red")
                tcp_socket.close()
                return

            # Determine Content-Type and set UTF-8 encoding for text content
            content_type = get_content_type(file_path)
            if content_type.startswith("text/"):
                content_type += "; charset=utf-8"

            # Build HTTP response headers
            response_header = 'HTTP/1.1 200 OK\r\n'
            response_header += f'Content-Type: {content_type}\r\n'
            response_header += f'Content-Length: {len(response_body)}\r\n'
            response_header += 'Connection: close\r\n\r\n'

            # Send response header and body
            tcp_socket.sendall(response_header.encode() + response_body)
            log_message(f"{client_ip} - File Served: {file_path} (200)", "green")

        except FileNotFoundError:
            response_header = 'HTTP/1.1 404 Not Found\r\n\r\n'
            response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
            tcp_socket.sendall(response_header.encode() + response_body)
            log_message(f"{client_ip} - File Not Found (404)", "orange")

        except PermissionError:
            response_header = 'HTTP/1.1 403 Forbidden\r\n\r\n'
            response_body = b"<html><body><h1>403 Forbidden</h1></body></html>"
            tcp_socket.sendall(response_header.encode() + response_body)
            log_message(f"{client_ip} - Permission Denied (403)", "red")

    except Exception as e:
        log_message(f"Error handling request from {client_address}: {e}", "red")
        tcp_socket.sendall("HTTP/1.1 500 Internal Server Error\r\n\r\n".encode())
    finally:
        tcp_socket.close()

# Server startup function
def start_server():
    global is_running
    status_label.config(text="Server Status: Running", fg="green")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    threading.Thread(target=start_server).start()

def stop_server():
    global is_running
    is_running = False
    status_label.config(text="Server Status: Stopped", fg="red")
    log_message("Server stopping...", "red")

# Buttons to start and stop the server
start_button = tk.Button(root, text="Start Server", command=start_server_thread, bg="green", fg="white")
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Server", command=stop_server, bg="red", fg="white")
stop_button.pack(pady=5)

# Run the GUI main loop
root.mainloop()
