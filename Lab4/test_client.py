# import socket
# import os
#
# # Configuration for server
# SERVER_HOST = '127.0.0.1'
# SERVER_PORT = 8080
# DEFAULT_FILE = '/index.html'
#
#
# # Helper function to send HTTP request and print the response
# def send_request(file_path):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#         client_socket.connect((SERVER_HOST, SERVER_PORT))
#         request = f"GET {file_path} HTTP/1.1\r\nHost: {SERVER_HOST}\r\nConnection: close\r\n\r\n"
#         client_socket.sendall(request.encode())
#
#         response = b""
#         while True:
#             data = client_socket.recv(1024)
#             if not data:
#                 break
#             response += data
#         print(response.decode())
#
#
# # Test Case 1: Valid Request (Expected: 200 OK)
# print("Test Case 1: Valid Request")
# send_request(DEFAULT_FILE)
#
# # Test Case 2: File Not Found (Expected: 404 Not Found)
# print("Test Case 2: File Not Found")
# send_request('/nonexistent.html')
#
# # Test Case 3: Permission Denied (Simulate by creating a file with restricted permissions)
# print("Test Case 3: Permission Denied")
# protected_file = 'protected.html'
# with open(protected_file, 'w') as file:
#     file.write("<html><body>Protected Content</body></html>")
# os.chmod(protected_file, 0o000)  # Remove all permissions
# send_request('/' + protected_file)
# os.chmod(protected_file, 0o644)  # Restore permissions
#
# # Test Case 4: Large File Content (Simulate with a large HTML file)
# # print("Test Case 4: Large File Content")
# # large_file = 'large.html'
# # with open(large_file, 'w') as file:
# #     file.write("<html><body>" + "A" * 10 ** 6 + "</body></html>")  # 1 MB file
# # send_request('/' + large_file)
#
# # Test Case 5: Invalid Request Format (Expected: error handling for bad request)
# print("Test Case 5: Invalid Request Format")
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#     client_socket.connect((SERVER_HOST, SERVER_PORT))
#     bad_request = "INVALID / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(SERVER_HOST)
#     client_socket.sendall(bad_request.encode())
#     response = client_socket.recv(1024)
#     print(response.decode())
#
# # Test Case 6: Path Traversal Attack (Expected: Prevent Access, maybe 403 Forbidden or 404 Not Found)
# print("Test Case 6: Path Traversal Attack")
# send_request('/../etc/passwd')
#
# # # Test Case 7: Character Encoding Check (Ensure server response encoding is consistent)
# print("Test Case 7: Character Encoding Check")
# send_request('/' + DEFAULT_FILE)
# #
# # # Clean up generated test files
# os.remove(protected_file)
# # os.remove(large_file)




import socket
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Configuration for server
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
DEFAULT_FILE = '/index.html'

# Helper function to send HTTP request and get the response
def send_request(file_path, output_text):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        request = f"GET {file_path} HTTP/1.1\r\nHost: {SERVER_HOST}\r\nConnection: close\r\n\r\n"
        client_socket.sendall(request.encode())

        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data
        output_text.insert(tk.END, response.decode() + "\n\n")

# Function for each test case
def test_valid_request(output_text):
    output_text.insert(tk.END, "Test Case 1: Valid Request\n", 'header')
    send_request(DEFAULT_FILE, output_text)

def test_file_not_found(output_text):
    output_text.insert(tk.END, "Test Case 2: File Not Found\n", 'header')
    send_request('/nonexistent.html', output_text)

def test_permission_denied(output_text):
    output_text.insert(tk.END, "Test Case 3: Permission Denied\n", 'header')
    protected_file = 'protected.html'
    with open(protected_file, 'w') as file:
        file.write("<html><body>Protected Content</body></html>")
    os.chmod(protected_file, 0o000)  # Remove all permissions
    send_request('/' + protected_file, output_text)
    os.chmod(protected_file, 0o644)  # Restore permissions

def test_invalid_request_format(output_text):
    output_text.insert(tk.END, "Test Case 5: Invalid Request Format\n", 'header')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        bad_request = "INVALID / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(SERVER_HOST)
        client_socket.sendall(bad_request.encode())
        response = client_socket.recv(1024)
        output_text.insert(tk.END, response.decode() + "\n\n")

def test_path_traversal_attack(output_text):
    output_text.insert(tk.END, "Test Case 6: Path Traversal Attack\n", 'header')
    send_request('/../etc/passwd', output_text)

def test_character_encoding_check(output_text):
    output_text.insert(tk.END, "Test Case 7: Character Encoding Check\n", 'header')
    send_request('/' + DEFAULT_FILE, output_text)

# UI Setup with enhanced styling
def setup_ui():
    root = tk.Tk()
    root.title("HTTP Client Test Interface")
    root.geometry("700x600")
    root.configure(bg="#f0f0f0")  # Light background

    # Instructions label
    instruction_label = tk.Label(root, text="Select a test case to send HTTP request to the server and view the response.",
                                 font=("Helvetica", 12, "bold"), bg="#f0f0f0", fg="#333333")
    instruction_label.pack(pady=10)

    # Buttons frame
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=10)

    # Styled buttons
    button_style = {"padx": 10, "pady": 5, "font": ("Helvetica", 10, "bold"), "bg": "#4CAF50", "fg": "#ffffff"}
    btn_valid_request = tk.Button(button_frame, text="Test Case 1: Valid Request", command=lambda: test_valid_request(output_text), **button_style)
    btn_file_not_found = tk.Button(button_frame, text="Test Case 2: File Not Found", command=lambda: test_file_not_found(output_text), **button_style)
    btn_permission_denied = tk.Button(button_frame, text="Test Case 3: Permission Denied", command=lambda: test_permission_denied(output_text), **button_style)
    btn_invalid_request_format = tk.Button(button_frame, text="Test Case 5: Invalid Request Format", command=lambda: test_invalid_request_format(output_text), **button_style)
    btn_path_traversal_attack = tk.Button(button_frame, text="Test Case 6: Path Traversal Attack", command=lambda: test_path_traversal_attack(output_text), **button_style)
    btn_character_encoding_check = tk.Button(button_frame, text="Test Case 7: Character Encoding Check", command=lambda: test_character_encoding_check(output_text), **button_style)

    # Arrange buttons in a grid layout
    btn_valid_request.grid(row=0, column=0, padx=5, pady=5)
    btn_file_not_found.grid(row=0, column=1, padx=5, pady=5)
    btn_permission_denied.grid(row=0, column=2, padx=5, pady=5)
    btn_invalid_request_format.grid(row=1, column=0, padx=5, pady=5)
    btn_path_traversal_attack.grid(row=1, column=1, padx=5, pady=5)
    btn_character_encoding_check.grid(row=1, column=2, padx=5, pady=5)

    # Output area for server response with enhanced styling
    output_text = scrolledtext.ScrolledText(root, width=85, height=20, wrap=tk.WORD, font=("Courier New", 10))
    output_text.pack(pady=10)
    output_text.tag_config('header', foreground='blue', font=("Helvetica", 10, "bold"))

    # Run the Tkinter main loop
    root.mainloop()

# Run the UI
if __name__ == "__main__":
    setup_ui()
