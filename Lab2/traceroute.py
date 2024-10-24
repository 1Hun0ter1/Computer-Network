

""""
1.跳数（hop count）表示数据包从源主机到目标主机之间经过的路由器或网络设备的数量。每经过一个中间设备（如路由器、交换机等），就是一次“跳”，因此跳数会增加。

2.在网络中，数据包从源主机到达目标主机时，通常不会直接到达，而是经过多个中间路由器，每经过一个路由器，TTL（Time to Live，生存时间）值会减一。
当 TTL 值变为 0 时，当前的路由器会丢弃数据包并返回一个 ICMP "TTL exceeded" 消息给发送者。
因此，跳数增加意味着数据包经过了更多的中间路由器或设备，每增加一次跳数，数据包会比之前走得更远一段距离。
3.
(1)TTL：每次 traceroute 增加 TTL 值并发送 ICMP 数据包。TTL 初始值为 1，代表数据包只能经过 1 个设备。
当数据包到达第一个路由器时，TTL 减为 0，路由器返回“TTL exceeded”消息。这时，我们知道第一个设备的 IP 地址。
(2)增加 TTL：TTL 逐步增加为 2、3、4 等等。每当 TTL 增加，数据包可以到达更远的设备并得到该设备的回应。
(3)最终目的地：当 TTL 足够大，数据包最终会到达目标主机，收到的是 ICMP Echo Reply，而不是“TTL exceeded”，这表明数据包成功到达目的地，traceroute 终止。

"""

import socket
import struct
import time
import os
import argparse
import threading
import json
import csv
import matplotlib.pyplot as plt

from _socket import IPPROTO_IP, IP_TTL


from colorama import Fore, Style, init
from queue import Queue
from tqdm import tqdm



# Initialization of colorama
init(autoreset=True)




# Helper function to calculate checksum
def calculate_checksum(source_string):
    count_to = (len(source_string) // 2) * 2
    checksum = 0
    count = 0

    while count < count_to:
        # val = (source_string[count]) << 8 + source_string[count + 1]  # 小端序，高字节在后，低字节在前
        val = source_string[count + 1] * 256 + source_string[count] # 大端序，高字节在前，低字节在后
        checksum = checksum + val
        checksum = checksum & 0xffffffff
        count += 2

    if count_to < len(source_string):
        checksum += (source_string[len(source_string) - 1])
        checksum = checksum & 0xffffffff

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += (checksum >> 16)
    result = ~checksum
    result = result & 0xffff
    result = result >> 8 | (result << 8 & 0xff00)
    return result


# Create ICMP Echo Request packet
def create_icmp_packet(packet_id):
    # Hearder is type(8), code(0), checksum,
    header = struct.pack('!BBHHH', 8, 0, 0, packet_id, 1)
    data = struct.pack('d', time.time())
    checksum = calculate_checksum(header + data)
    header = struct.pack('!BBHHH', 8, 0, checksum, packet_id, 1)
    return header + data


# Create UDP packet (alternative to ICMP)
def create_udp_packet():
    # header = struct.pack('!HHHH', 33434, packet_id, 0, 0)  [打包的数据类型有问题，length，校验和没有更新]
    # data = b'PING'  # Can be extended to send custom payload

    src_port = 33434
    dst_port = 33434
    data = os.urandom(32)

    length = 8 + len(data)

    header = struct.pack('!HHHH', src_port, dst_port, length, 0)
    # data = b'PING' * 3

    checksum = calculate_checksum(header + data)
    header = struct.pack('!HHHH', src_port, dst_port, length, checksum)

    return header + data


# Send ICMP packet and return the time it was sent
def send_packet(sock, dest_addr, packet_id, ttl, dst_port, use_icmp=True):
    try:
        # sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl) # 不同操作系统，PC可能会出错，【 win Error 10022 】

        sock.setsockopt(IPPROTO_IP, IP_TTL, struct.pack("I",ttl))

        if use_icmp:
            packet = create_icmp_packet(packet_id)
        else:
            packet = create_udp_packet()

        time_sent = time.time()

        # 用法： sock.sendto(data, (address, port))

        # 1 if use_icmp：当使用 ICMP 协议时，端口号设为 1，这是一个虚拟端口，因 ICMP 协议不需要实际的传输层端口
        # else dst_port：当使用 UDP 协议时，必须为目标地址提供有效的 UDP 端口号（即 dst_port）。

        # sock.sendto(packet, (dest_addr, 1 if use_icmp else 33434))
        sock.sendto(packet, (dest_addr, 1 if use_icmp else dst_port))
        #
        # print(f"Sent packet: {packet} to {dest_addr} with TTL={ttl}")
        return time_sent
    except OSError as e:
        print(f"Send packet failed with error: {e}")
        return None


# Receive ICMP response and measure RTT
def receive_packet(sock, packet_id, timeout, send_time, use_icmp):
    sock.settimeout(timeout)

    try:
        # start_time = time.time()
        recv_packet, addr = sock.recvfrom(1024)
        # [到这里会直接抛出异常，socket_timeout, 即丢包？]
        # [WinError 10052]
        # print(f"Received packet from {addr}")


        # 记录包的源端口和目的端口
        src_port, dst_port = struct.unpack('!HH', recv_packet[:4])
        # 如果端口号为 53，表明是 DNS 数据包，忽略该包
        if src_port == 53 or dst_port == 53:
            print(f"Received a DNS packet from {addr}, ignoring...")
            return None, None

        time_received = time.time()

        icmp_header = recv_packet[20:28]
        icmp_type, code, checksum, recv_id, seq = struct.unpack('!BBHHH', icmp_header)

        # if recv_id == packet_id and (icmp_type == 0 or icmp_type == 11):
        #     return addr[0], (time.time() - start_time) * 1000
        # return None, None
        if use_icmp:
            if icmp_type == 0 and recv_id == packet_id:
                # If it's ICMP Echo Reply and ID matches, return RTT and address
                return addr[0], (time_received - send_time) * 1000
            elif icmp_type == 11:
                # If it's TTL Exceeded message, handle without ID check
                return addr[0], (time_received - send_time) * 1000
            elif icmp_type == 3:
                # Destination Unreachable
                if code == 3:
                    # Port unreachable (most common case for traceroute using UDP)
                    return addr[0], (time_received - send_time) * 1000
                else:
                    # print(f"ICMP Destination Unreachable received, code: {code}")
                    print(Fore.RED + f"ICMP Unreachable   ", end='')
                    return None, None
            else:
                # Handle other ICMP types
                # print(f"Unhandled ICMP type: {icmp_type}, code: {code}")
                print(Fore.RED + f"Unhandled ICMP type: {icmp_type}, code: {code}   ", end='')
                return None, None
        else:
            # For UDP - expect ICMP Destination Unreachable (Type 3, Code 3)
            if icmp_type == 3 and code == 3:
                # ICMP Type 3: Destination Unreachable, Code 3: Port Unreachable
                return addr[0], (time_received - send_time) * 1000
            elif icmp_type == 11:
                # ICMP Type 11: TTL Exceeded
                return addr[0], (time_received - send_time) * 1000
            elif icmp_type == 1:
                # ICMP Redirect message
                # print(f"ICMP Redirect received from {addr[0]}, redirect code: {code}")
                print(Fore.RED + f"ICMP Redirect received from {addr[0]}, redirect code: {code}   ", end='')
                return addr[0], (time_received - send_time) * 1000
            else:
                # print(f"Unhandled ICMP type in UDP mode: {icmp_type}, code: {code}")
                print(Fore.RED + f"Unhandled ICMP type in UDP mode: {icmp_type}, code: {code}   ", end='')
                return None, None
# """"""
# 不需要对TTL exceeded 的消息做严格的 id 判断
# """
        # if icmp_type == 0 and recv_id == packet_id:
        #     # 如果是 ICMP Echo Reply 并且 ID 匹配，则返回 RTT 和地址
        #     return addr[0], (time.time() - start_time) * 1000
        # elif icmp_type == 11:
        #     # 如果是 TTL Exceeded 消息，不需要检查 ID，直接处理
        #     return addr[0], (time.time() - start_time) * 1000
        # else:
        #     # 其他类型的消息，忽略
        #     return None, None


    except socket.timeout:
        # print(f"Socket timeout")
        print(Fore.BLUE + f"Socket timeout       ", end='')
        return None, None
    except OSError as e:
        # print(f"OSError occurred: {e}")  # 捕获其他socket错误
        print(Fore.BLUE + f"OSError occurred: {e}  ", end='')  # 捕获其他socket错误
        return None, None




# Threaded traceroute function per TTL
def traceroute_ttl_thread(dest_ip, ttl, retries, timeout, result_queue, use_icmp):
    rtt_list = []
    addr = None
    for retry in range(retries):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW if use_icmp else socket.SOCK_DGRAM, socket.IPPROTO_ICMP if use_icmp else socket.IPPROTO_UDP)
        sock.bind(("", 0))

        dst_port = 40000 + ttl  # Dynamic destination port for UDP
        packet_id = os.getpid() & 0xFFFF
        send_time = send_packet(sock, dest_ip, packet_id, ttl, dst_port, use_icmp)
        addr, rtt = receive_packet(sock, packet_id, timeout, send_time, use_icmp)
        sock.close()

        if addr:
            rtt_list.append(rtt)
            if addr == dest_ip:
                result_queue.put((ttl, addr, rtt_list))
                return
        # Retry logic
        print(f"Retrying TTL {ttl}, attempt {retry + 1}/{retries}")

    # If no valid response after retries, put None
    result_queue.put((ttl, addr, rtt_list if addr else None))


# Main Traceroute function
def traceroute(dest_addr, max_hops=30, timeout=1, retries=3, use_icmp=True, async_mode=False, save_format=None):
    try:
        dest_ip = socket.gethostbyname(dest_addr)
        print(f'Traceroute to {dest_ip} ({dest_addr}), {max_hops} hops max')

        result_queue = Queue()
        threads = []

        # Create threads for each TTL (hop) if async_mode is enabled
        if async_mode:
            avg_rtts_per_hop = []  # 保存每跳的平均 RTT

            pbar = tqdm(total=max_hops, desc=f"Tracing {dest_addr}")
            # Create threads for each TTL (hop)
            for ttl in range(1, max_hops + 1):
                thread = threading.Thread(target=traceroute_ttl_thread, args=(dest_ip, ttl, retries, timeout, result_queue, use_icmp))
                threads.append(thread)
                thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join()
                pbar.update(1)

            pbar.close()

            results = []
            while not result_queue.empty():
                ttl, addr, rtt_list = result_queue.get()
                if addr:
                    if rtt_list:
                        avg_rtt = sum(rtt_list) / len(rtt_list)
                        print(f"{ttl}: {addr} - RTTs: {rtt_list} (Average RTT: {avg_rtt:.3f} ms)")
                    results.append((ttl, addr, rtt_list))
                    avg_rtts_per_hop.append(avg_rtt)
                else:
                    print(f"{ttl}: *")

            if save_format:
                save_results(results, dest_addr, save_format)

            # plot_traceroute_results(results, dest_addr)

            plot_avg_rtt(avg_rtts_per_hop, dest_addr)
        else:
            des_flag = False  # destination stop flag
            results = []
            pbar = tqdm(total=max_hops, desc=f"Tracing {dest_addr}")

            for ttl in range(1, max_hops + 1):
                rtt_list = []
                reached_dest = False
                print(f'\nTTL {ttl:<2}:   ', end='')
                InitialAddr = None
                InitialHostname = None

                for retry in range(retries):

                    # sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                    #                      socket.IPPROTO_ICMP if use_icmp else socket.IPPROTO_UDP)


                    if use_icmp:#socket.AF_INET：表示使用 IPv4 地址
                        # ICMP 使用 RAW socket
                        #socket.SOCK_RAW：表示使用原始套接字，允许手动构造 IP 包
                        #socket.IPPROTO_ICMP：表示使用 ICMP 协议，通常用于发送 ICMP 请求
                        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                    else:
                        # UDP 使用 Datagram (SOCK_DGRAM)
                        #socket.SOCK_DGRAM：表示使用DGRAM套接字。UDP 是一种无连接的、不可靠的传输层协议，用于发送数据报文（Datagram），因此数据包不保证到达目的地或按顺序到达。
                        #socket.IPPROTO_UDP：表示使用 UDP 协议。这一参数规定了套接字所使用的底层传输协议为 UDP。
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

                    # "" 表示绑定到本地所有可用的网络接口； 0 表示让系统为这个 socket 动态选择一个可用的本地端口
                    sock.bind(("", 0))  # 动态分配本地端口

                    # dst_port = 33434 + ttl  # 动态目标端口
                    dst_port = 40000 + ttl  # 动态目标端口

                    packet_id = os.getpid() & 0xFFFF

                    send_time = send_packet(sock, dest_ip, packet_id, ttl, dst_port, use_icmp)

                    addr, rtt = receive_packet(sock, packet_id, timeout, send_time, use_icmp)
                    sock.close()


                    if addr:
                        try:
                            hostname = socket.gethostbyaddr(addr)[0]
                            # hostname: '10.148.0.1'
                        except socket.herror:
                            hostname = addr
                            InitialHostname = hostname
                            InitialAddr = addr
                        # print(f'{ttl} {hostname} ({addr})  rtt={rtt:.3f} ms')
                        print(f'{rtt:10.3f} ms       ', end='')
                        rtt_list.append(rtt)



                # if reached_dest:
                #     break

                    if retry == retries - 1:
                        if InitialHostname == None:
                            print(Fore.YELLOW + 'None          ', end='')
                        elif InitialHostname == InitialAddr:
                            print(Fore.GREEN + f'{InitialAddr}', end='')
                        else:
                            print(Fore.GREEN + f'{InitialHostname} ({InitialAddr})', end='')

                        print(Fore.YELLOW + f"    Packet loss rate: {((retries - len(rtt_list)) / retries) * 100:.1f}%")

                        if InitialAddr == dest_ip:

                            if des_flag is False:
                                print(Fore.GREEN + "\nWe've reached our destination!")  # 打印“到达终点了！”的提示
                                des_flag = True

                                pbar.close()

                            reached_dest = True

                results.append((ttl, addr, rtt_list))

                pbar.update(1)

                time.sleep(0.5)

                if reached_dest and retry == retries - 1:
                    print(Fore.YELLOW + f"\nTraceroute to {dest_ip} ({dest_addr}) over!")
                    break

            if not reached_dest:
                print(Fore.RED + f"Failed to reach {dest_addr} ({dest_ip}) within {max_hops} hops.")

            if save_format:
                save_results(results, dest_addr, save_format)

            plot_traceroute_results(results, dest_addr)


    except socket.gaierror:
        print(f'Cannot resolve {dest_addr}, aborting...')



def save_results(results, dest_addr, save_format):
    if save_format == "csv":
        with open(f"traceroute_results_{dest_addr}.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Hop", "IP Address", "RTTs (ms)"])
            for ttl, addr, rtt_list in results:
                writer.writerow([ttl, addr, rtt_list])
        print(Fore.GREEN + f"Results saved to traceroute_results_{dest_addr}.csv")
    elif save_format == "json":
        data = {"destination": dest_addr, "hops": []}
        for ttl, addr, rtt_list in results:
            data["hops"].append({"hop": ttl, "ip": addr, "rtts": rtt_list})
        with open(f"traceroute_results_{dest_addr}.json", "w") as file:
            json.dump(data, file, indent=4)
        print(Fore.GREEN + f"Results saved to traceroute_results_{dest_addr}.json")

def plot_avg_rtt(avg_rtts_per_hop, target_ip):
    hops = list(range(1, len(avg_rtts_per_hop) + 1))  # 创建跳数列表
    plt.figure(figsize=(10, 5))
    plt.plot(hops, avg_rtts_per_hop, marker='o', linestyle='-', color='b')  # 绘制折线图
    plt.title(f"Average RTT per Hop for {target_ip}")
    plt.xlabel("Hop Count")
    plt.ylabel("Average RTT (ms)")
    plt.grid(True)
    plt.show()
def plot_traceroute_results(results, target_ip):
    ttls = [res[0] for res in results]
    avg_rtts = [sum(res[2]) / len(res[2]) if res[2] else 0 for res in results]

    plt.figure(figsize=(10, 5))
    plt.plot(ttls, avg_rtts, marker='o')
    plt.title(f"Traceroute RTT per Hop for {target_ip}")
    plt.xlabel("Hop Count")
    plt.ylabel("Average RTT (ms)")
    plt.grid(True)
    plt.show()

# Command-line argument parser
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Traceroute tool using ICMP or UDP")
    parser.add_argument('--destination', help="Destination address or hostname")
    parser.add_argument('--max-hops', type=int, default=30, help="Max number of hops to trace")
    parser.add_argument('--timeout', type=float, default=1, help="Timeout for each hop in seconds")
    parser.add_argument('--retries', type=int, default=3, help="Retries per hop")
    parser.add_argument('--protocol', choices=['ICMP', 'UDP'], default='ICMP', help="Use ICMP or UDP for tracing")
    parser.add_argument('--save-format', choices=['csv', 'json'], help="Save results in CSV or JSON format")
    parser.add_argument('--async-mode', action='store_true', help="Enable asynchronous (multi-threaded) mode")

    args = parser.parse_args()

    use_icmp = args.protocol == 'ICMP'
    traceroute(args.destination, args.max_hops, args.timeout, args.retries, use_icmp, async_mode=args.async_mode, save_format=args.save_format)

    #python traceroute.py --destination www.youku.com --max-hops 30 --timeout 5 --retries 3 --protocol ICMP --save-format json （单线程)
    #python traceroute.py --destination www.youku.com --max-hops 30 --timeout 5 --retries 3 --protocol ICMP --save-format json --async-mode(多线程)
    #python traceroute.py --destination www.youku.com --max-hops 30 --timeout 3 --retries 3 --protocol UDP (Only in Linux)