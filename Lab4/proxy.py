import socket
import threading
import logging
import os
import tkinter as tk
from tkinter import scrolledtext

# Proxy configuration
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 8001
MAX_CONNECTIONS = 5
CACHE_DIR = './cache'

# Global variables for server control
is_running = False

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Function to fetch content from the actual server
def fetch_from_server(server_host, server_port, method, path, body=None):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect((server_host, server_port))

            # Construct the request to the web server
            request = f"{method} {path} HTTP/1.1\r\nHost: {server_host}\r\nConnection: close\r\n"
            if body:
                request += f"Content-Length: {len(body)}\r\n"
            request += "\r\n"
            if body:
                request += body

            server_socket.sendall(request.encode())

            # Fetch response from server
            response = b""
            while True:
                data = server_socket.recv(1024)
                if not data:
                    break
                response += data

            return response
    except Exception as e:
        log_message(f"Error fetching from server: {e}", "red")
        return None

# Proxy request handler
def handle_request(client_socket):
    global request_count
    try:
        request = client_socket.recv(1024).decode()
        request_lines = request.splitlines()
        if len(request_lines) == 0:
            return

        # Parse the HTTP request line
        request_line = request_lines[0]
        method, path, _ = request_line.split()

        # Forward requests to a predefined server
        web_server_host = '127.0.0.1'
        web_server_port = 8080

        # Determine cache file path
        cache_file_path = os.path.join(CACHE_DIR, path.strip('/'))
        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        if method == "GET":
            if os.path.exists(cache_file_path):
                log_message(f"Cache hit for {path}", "green")
                with open(cache_file_path, 'rb') as f:
                    response = f.read()
            else:
                log_message(f"Cache miss for {path}. Fetching from server.", "orange")
                response = fetch_from_server(web_server_host, web_server_port, method, path)
                if response:
                    status_line = response.split(b"\r\n", 1)[0].decode()
                    if "200 OK" in status_line:
                        with open(cache_file_path, 'wb') as f:
                            f.write(response)
        elif method in ["POST", "PUT", "DELETE"]:
            body = None
            if "Content-Length" in request:
                content_length = int([line.split(": ")[1] for line in request_lines if "Content-Length" in line][0])
                headers_end = request.find("\r\n\r\n") + 4
                body = request[headers_end:headers_end + content_length]
            response = fetch_from_server(web_server_host, web_server_port, method, path, body)
        else:
            response = b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"

        if response:
            client_socket.sendall(response)

    except Exception as e:
        log_message(f"Error handling request: {e}", "red")
        client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
    finally:
        client_socket.close()

# GUI functions
def log_message(message, color="black"):
    log_area.config(state='normal')
    log_area.insert(tk.END, message + "\n", ("color",))
    log_area.tag_config("color", foreground=color)
    log_area.config(state='disabled')
    log_area.see(tk.END)

def start_proxy():
    global is_running
    if is_running:
        log_message("Server is already running!", "orange")
        return

    is_running = True
    log_message(f"Proxy server starting on {PROXY_HOST}:{PROXY_PORT}", "blue")
    threading.Thread(target=run_proxy_server, daemon=True).start()

def stop_proxy():
    global is_running
    is_running = False
    log_message("Proxy server stopping...", "red")

def run_proxy_server():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_HOST, PROXY_PORT))
    proxy_socket.listen(MAX_CONNECTIONS)
    log_message(f"Proxy server running on {PROXY_HOST}:{PROXY_PORT}", "blue")

    try:
        while is_running:
            client_socket, client_address = proxy_socket.accept()
            log_message(f"Connection received from {client_address}", "green")
            threading.Thread(target=handle_request, args=(client_socket,)).start()
    except Exception as e:
        log_message(f"Error: {e}", "red")
    finally:
        proxy_socket.close()
        log_message("Proxy server stopped", "red")

# GUI setup
root = tk.Tk()
root.title("Proxy Server")
root.geometry("400x500")

# Log display area
log_area = scrolledtext.ScrolledText(root, width=90, height=30, state='disabled', wrap=tk.WORD)
log_area.pack(pady=10)

# Buttons
start_button = tk.Button(root, text="Start Proxy", command=start_proxy, bg="green", fg="white")
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Proxy", command=stop_proxy, bg="red", fg="white")
stop_button.pack(pady=5)

root.mainloop()
