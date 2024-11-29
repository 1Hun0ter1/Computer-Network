import socket
import threading
import logging
import os
import tkinter as tk
from tkinter import scrolledtext

# Global variables for server control
is_running = False

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Default values
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 8001
MAX_CONNECTIONS = 5
CACHE_DIR = './cache'
DOWNLOAD_DIR = './downloads'  # Directory to save downloaded images

# Function to fetch content from the actual server
def fetch_from_server(server_host, server_port, method, path, body=None):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # DNS resolution
            server_ip = socket.gethostbyname(server_host)
            server_socket.connect((server_ip, server_port))

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
    except socket.gaierror:
        log_message(f"DNS resolution failed for {server_host}", "red")
        return b"HTTP/1.1 502 Bad Gateway\r\n\r\n"
    except Exception as e:
        log_message(f"Error fetching from server: {e}", "red")
        return b"HTTP/1.1 500 Internal Server Error\r\n\r\n"


# Proxy request handler
def handle_request(client_socket):
    try:
        request = client_socket.recv(1024).decode(errors="replace")
        request_lines = request.splitlines()
        if len(request_lines) == 0:
            return

        # Parse the HTTP request line
        request_line = request_lines[0]
        method, path, _ = request_line.split()

        # Extract Host header
        host_line = [line for line in request_lines if line.lower().startswith("host:")]
        if not host_line:
            client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\nMissing Host header")
            return
        host = host_line[0].split(":", 1)[1].strip()  # Initial extraction

        if host.startswith("http://") or host.startswith("https://"):
            host = host.split("://", 1)[1]  # Remove protocol part

        # Remove port if present in host
        host = host.split("/", 1)[0]  # Take only the hostname (remove trailing paths)

        # Determine target server
        if host == "127.0.0.1":
            web_server_host = "127.0.0.1"
            web_server_port = 8080
        else:
            web_server_host = host
            web_server_port = 80  # Default HTTP port

        # Create cache key using Host + Path
        cache_key = f"{host}{path}"
        cache_file_path = os.path.join(CACHE_DIR, cache_key.strip('/').replace("/", "_"))
        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        # Handle GET requests with caching
        if method == "GET":
            if os.path.exists(cache_file_path):
                log_message(f"Cache hit for {path} on {host}", "green")
                with open(cache_file_path, 'rb') as f:
                    response = f.read()
            else:
                log_message(f"Cache miss for {path} on {host}. Fetching from server.", "orange")
                response = fetch_from_server(web_server_host, web_server_port, method, path)
                if response:
                    # Extract status line and content type
                    status_line = response.split(b"\r\n", 1)[0].decode()
                    if "200 OK" in status_line:
                        with open(cache_file_path, 'wb') as f:
                            f.write(response)

        # Handle POST, PUT, DELETE requests
        elif method in ["POST", "PUT", "DELETE"]:
            body = None
            if "Content-Length" in request:
                content_length = int([line.split(": ")[1] for line in request_lines if "Content-Length" in line][0])
                headers_end = request.find("\r\n\r\n") + 4
                body = request[headers_end:headers_end + content_length]
            response = fetch_from_server(web_server_host, web_server_port, method, path, body)
        else:
            response = b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"

        # Send response back to client
        if response:
            client_socket.sendall(response)

            # Parse headers to check for Content-Type
            response_headers, response_body = response.split(b"\r\n\r\n", 1)
            headers = response_headers.decode().split("\r\n")
            content_type_line = [line for line in headers if line.lower().startswith("content-type:")]

            if content_type_line:
                content_type = content_type_line[0].split(":")[1].strip()
                if content_type.startswith("image/"):  # Check if the response is an image
                    # Extract file extension from Content-Type
                    file_extension = content_type.split("/")[-1]
                    if not file_extension:
                        file_extension = "png"  # Default to PNG if no extension is found

                    # Ensure download directory exists
                    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

                    # Save image to local disk
                    filename = path.split("/")[-1] or f"downloaded_image.{file_extension}"
                    filepath = os.path.join(DOWNLOAD_DIR, filename)
                    with open(filepath, "wb") as image_file:
                        image_file.write(response_body)

                    log_message(f"Image saved as {filepath}", "green")

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


# Function to start the proxy server with custom inputs from UI
def start_proxy():
    global PROXY_HOST, PROXY_PORT, MAX_CONNECTIONS, is_running

    # Get values from the UI
    PROXY_HOST = proxy_ip_entry.get()
    PROXY_PORT = int(proxy_port_entry.get())
    MAX_CONNECTIONS = int(max_connections_entry.get())

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
root.geometry("400x550")

# Log display area
log_area = scrolledtext.ScrolledText(root, width=70, height=15, state='disabled', wrap=tk.WORD)
log_area.pack(pady=10)

# Buttons and input fields
tk.Label(root, text="Proxy IP:").pack(pady=5)
proxy_ip_entry = tk.Entry(root)
proxy_ip_entry.insert(0, "127.0.0.1")
proxy_ip_entry.pack(pady=5)

tk.Label(root, text="Proxy Port:").pack(pady=5)
proxy_port_entry = tk.Entry(root)
proxy_port_entry.insert(0, "8001")
proxy_port_entry.pack(pady=5)

tk.Label(root, text="Max Connections:").pack(pady=5)
max_connections_entry = tk.Entry(root)
max_connections_entry.insert(0, "5")
max_connections_entry.pack(pady=5)

start_button = tk.Button(root, text="Start Proxy", command=start_proxy, bg="green", fg="white")
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Proxy", command=stop_proxy, bg="red", fg="white")
stop_button.pack(pady=10)

root.mainloop()
