import socket
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import os

# Directory to save images
DOWNLOAD_DIR = "./downloads"

# Send HTTP request
def send_request(serverAddress, serverPort, method, file_path, host, body=None):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Set a timeout to prevent hanging
            client_socket.settimeout(10)
            client_socket.connect((serverAddress, serverPort))

            # Build HTTP request
            request = f"{method} {file_path} HTTP/1.1\r\nHost: {host}\r\n"
            if method in ["POST", "PUT"] and body:
                request += f"Content-Length: {len(body)}\r\n\r\n{body}"
            else:
                request += "\r\n"

            print("Sending request:")
            print(request)

            client_socket.sendall(request.encode())

            # Receive response
            response = b""
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    response += data
                except socket.timeout:
                    break

            # Split headers and body
            headers, _, body = response.partition(b"\r\n\r\n")
            headers_str = headers.decode(errors="replace")

            # Check for content type in headers
            content_type = None
            for line in headers_str.split("\r\n"):
                if line.lower().startswith("content-type:"):
                    content_type = line.split(":")[1].strip()
                    break

            # If content type is image, save to file
            if content_type and content_type.startswith("image/"):
                file_extension = content_type.split("/")[-1]
                filename = file_path.split("/")[-1] or f"downloaded_image.{file_extension}"
                os.makedirs(DOWNLOAD_DIR, exist_ok=True)
                filepath = os.path.join(DOWNLOAD_DIR, filename)

                with open(filepath, "wb") as image_file:
                    image_file.write(body)
                return f"Image saved to {filepath}"

            # If not image, return response as string
            response_str = response.decode(errors="replace")  # Avoid decode errors
            return response_str
    except Exception as e:
        return f"Error: {e}"

# Simulate multiple clients
def simulate_multiple_clients(serverAddress, serverPort, method, file_path, host, num_clients, body=None):
    responses = []

    def threaded_request():
        response = send_request(serverAddress, serverPort, method, file_path, host, body)
        responses.append(response)
        if not response.startswith("Image saved to"):  # Only update UI for non-image responses
            root.after(0, update_response_display, response)

    threads = []
    for _ in range(num_clients):
        thread = threading.Thread(target=threaded_request)
        threads.append(thread)
        thread.start()

    return responses

# Update response display
def update_response_display(response):
    response_display.config(state="normal")
    response_display.insert(tk.END, response + "\n" + "-" * 80 + "\n")
    response_display.config(state="disabled")
    response_display.see(tk.END)

# Start simulation from UI
def start_simulation():
    serverAddress = proxy_ip_entry.get()
    serverPort = int(proxy_port_entry.get())
    method = method_combobox.get()
    file_path = file_path_entry.get()
    num_clients = int(num_clients_entry.get())
    host = host_entry.get().strip()
    body = body_text.get("1.0", tk.END).strip()

    # Ensure body is provided for POST/PUT
    if method in ["POST", "PUT"] and not body:
        messagebox.showwarning("Warning", f"{method} method requires a body. Please provide data.")
        return

    # Run simulation in a separate thread to prevent GUI blocking
    threading.Thread(
        target=simulate_multiple_clients,
        args=(serverAddress, serverPort, method, file_path, host, num_clients, body if body else None),
        daemon=True,
    ).start()

# Create GUI
root = tk.Tk()
root.title("HTTP Client Load Simulator")

# Proxy IP
tk.Label(root, text="Proxy/Server IP:").grid(row=0, column=0, padx=10, pady=5)
proxy_ip_entry = tk.Entry(root)
proxy_ip_entry.grid(row=0, column=1, padx=10, pady=5)
proxy_ip_entry.insert(0, "127.0.0.1")

# Proxy Port
tk.Label(root, text="Proxy/Server Port:").grid(row=1, column=0, padx=10, pady=5)
proxy_port_entry = tk.Entry(root)
proxy_port_entry.grid(row=1, column=1, padx=10, pady=5)
proxy_port_entry.insert(0, "8001")

# Host Header
tk.Label(root, text="Host (for remote):").grid(row=2, column=0, padx=10, pady=5)
host_entry = tk.Entry(root)
host_entry.grid(row=2, column=1, padx=10, pady=5)
host_entry.insert(0, "127.0.0.1")

# HTTP Method
tk.Label(root, text="HTTP Method:").grid(row=3, column=0, padx=10, pady=5)
method_combobox = ttk.Combobox(root, values=["GET", "POST", "PUT", "DELETE"], state="readonly")
method_combobox.grid(row=3, column=1, padx=10, pady=5)
method_combobox.set("GET")

# File Path
tk.Label(root, text="File Path:").grid(row=4, column=0, padx=10, pady=5)
file_path_entry = tk.Entry(root)
file_path_entry.grid(row=4, column=1, padx=10, pady=5)
file_path_entry.insert(0, "/index.html")

# Number of Clients
tk.Label(root, text="Number of Clients:").grid(row=5, column=0, padx=10, pady=5)
num_clients_entry = tk.Entry(root)
num_clients_entry.grid(row=5, column=1, padx=10, pady=5)
num_clients_entry.insert(0, "1")

# Request Body
tk.Label(root, text="Request Body (POST/PUT):").grid(row=6, column=0, padx=10, pady=5)
body_text = tk.Text(root, height=5, width=40)
body_text.grid(row=6, column=1, padx=10, pady=5)

# Start Button
start_button = tk.Button(root, text="Start Simulation", command=start_simulation, bg="green", fg="white")
start_button.grid(row=7, column=0, columnspan=2, pady=10)

# Response Display Area
tk.Label(root, text="Server Responses:").grid(row=8, column=0, padx=10, pady=5)
response_display = tk.Text(root, wrap=tk.WORD, width=80, height=35, state="disabled")
response_display.grid(row=25, column=0, columnspan=2, padx=10, pady=10)

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