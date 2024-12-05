import socket
import struct
import time
import os
import argparse
import threading

# 计算校验和的函数，用于ICMP数据包完整性验证
def calculate_checksum(source_string):
    """
    计算ICMP数据包的校验和，用于确保数据传输的完整性。

    :param source_string: 需要计算校验和的二进制字符串
    :return: 计算出来的校验和值
    """
    sum = 0
    count_to = (len(source_string) // 2) * 2
    count = 0

    # 以两个字节为单位计算和
    while count < count_to:
        # this_val = source_string[count + 1] * 256 + source_string[count]
        this_val = (source_string[count] << 8) + source_string[count + 1]
        sum += this_val
        sum &= 0xffffffff  # 保证和在32位内
        count += 2

    # 如果数据是奇数长度，则补上最后一个字节
    if count_to < len(source_string):
        sum += source_string[len(source_string) - 1]
        sum &= 0xffffffff

    # 将高位与低位相加
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)

    # 取反并返回校验和
    answer = ~sum
    answer = answer & 0xffff

    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


# 创建ICMP Echo Request数据包
def create_icmp_packet(packet_id, user_data):
    """
    创建ICMP回显请求数据包，包括计算校验和并填充头部。

    :param packet_id: 用于标识数据包的ID
    :param user_data: 用户自定义的字符串，将作为数据部分发送
    :return: 完整的ICMP数据包（二进制）
    """
    # ICMP头部（类型、代码、校验和、标识符、序列号）
    # ICMP类型为8（回显请求），我们将标识符设为packet_id，序列号设为1

    # 强制使用大端序 '!'
    header = struct.pack('!bbHHh', 8, 0, 0, packet_id, 1)

    # 数据部分包含当前时间戳，用于计算往返时间
    # data = struct.pack('d', time.time())

    # 将用户数据编码为字节串
    data = user_data.encode('utf-8')


    # 计算校验和（注意，校验和字段初始值为0）
    checksum = calculate_checksum(header + data)

    # 将计算出的校验和填充到ICMP头部
    header = struct.pack('!bbHHh', 8, 0, checksum, packet_id, 1)

    # 输出调试信息
    print("\n----- SENDING ICMP ECHO REQUEST -----")
    print(f"ICMP Type: 8 (Echo Request)\nID: {packet_id:#06x}\nSeq: 1")
    print(f"Checksum: {checksum:#06x}")
    print(f"Sending Data: {user_data}")
    print(f"Packet (hex): {header.hex() + data.hex()}")


    return header + data  # 返回完整的ICMP包


# 发送ICMP请求并接收回复
def send_one_ping(sock, dest_addr, packet_id, user_data):
    """
    向目标地址发送ICMP Echo Request数据包。

    :param sock: 已经创建好的socket对象
    :param dest_addr: 目标地址（IP）
    :param packet_id: 数据包的ID（用于匹配回显应答）
    :param user_data: 用户自定义的字符串，将作为数据部分发送
    :return: 发送的时间戳
    """
    # 创建ICMP数据包
    packet = create_icmp_packet(packet_id, user_data)

    # 记录发送时间
    time_sent = time.time()

    # 发送数据包到目标地址，端口号在ICMP协议中通常设置为1
    sock.sendto(packet, (dest_addr, 1))

    return time_sent

# 接收ICMP回显应答并处理
def receive_one_ping(sock, packet_id, timeout, user_data, time_sent):
    """
    等待并接收ICMP回显应答数据包，并计算往返时间。

    :param sock: 创建的套接字对象
    :param packet_id: 数据包的ID（用于匹配回显应答）
    :param timeout: 超时时间，以秒为单位
    :param user_data: 用户自定义的字符串，将作为数据部分发送
    :param time_sent: 发送的时间戳
    :return: 往返时间（毫秒），或者如果超时返回 None
    """
    # 设置套接字的超时时间
    sock.settimeout(timeout)
    try:
        # 从目标地址接收响应数据包
        recv_packet, addr = sock.recvfrom(1024)
        time_received = time.time()

        # 检查接收到的数据包长度是否足够容纳IP头部和ICMP头部（至少28字节）
        if len(recv_packet) < 28:
            print(f"接收到的数据包太小: {len(recv_packet)} 字节")
            return None

        # 提取并解析ICMP头部（从第21字节到第28字节）
        icmp_header = recv_packet[20:28]  # 前20个字节是IP头部，ICMP头部从第21个字节开始
        icmp_type, code, checksum, recv_id, sequence = struct.unpack('!bbHHh', icmp_header)

        # 匹配ID，并确认ICMP类型为0（表示回显应答）
        if recv_id == packet_id and icmp_type == 0:

            # # 获取发送时间（从第29字节开始）
            # time_sent = struct.unpack('d', recv_packet[28:28 + struct.calcsize('d')])[0]
            # 计算往返时间，并返回

            received_data = recv_packet[28:].decode('utf-8')

            # 输出接收到的数据调试信息
            print("\n----- RECEIVED ICMP ECHO REPLY -----")
            print(f"ICMP Type: {icmp_type} (Echo Reply)\nID: {recv_id:#06x}\nSeq: {sequence}")
            print(f"Checksum: {checksum:#06x}")
            print(f"Received Data: {received_data}")
            print(f"Packet (hex): {recv_packet.hex()}")


            if received_data == user_data:
                print("Data Match: ✅ ")
                # 计算往返时间，并返回
                return (time_received - time_sent) * 1000  # 返回毫秒
            else:
                print("Data Match: ❌ ")
                return None

        elif icmp_type == 3:
            # 目标不可达消息处理
            print(f"目标不可达，代码: {code}")
            return None
        elif icmp_type == 11:
            # 超时报文处理
            print(f"TTL 超时，代码: {code}")
            return None
        else:
            print(f"收到未知的 ICMP 消息，类型: {icmp_type}, 代码: {code}")
            return None
    except socket.timeout:
        print("请求超时。")
        return None  # 如果超时，返回 None


# 执行一次Ping操作
def do_one_ping(dest_addr, timeout=1, user_data="Ping"):
    """
    执行一次ping操作，发送ICMP Echo Request并接收Echo Reply。

    :param dest_addr: 目标主机地址
    :param timeout: 超时时间
    :param user_data: 用户自定义的字符串，将作为数据部分发送
    :return: 往返时间或None（如果超时）
    """
    try:
        # 创建SOCK_RAW套接字，使用ICMP协议
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except Exception as e:
        print(f"创建套接字失败: {e}")
        return None

    packet_id = os.getpid() & 0xFFFF  # 使用进程ID的低16位作为标识符
    time_sent = send_one_ping(sock, dest_addr, packet_id, user_data)  # 发送ping请求并记录发送时间
    delay = receive_one_ping(sock, packet_id, timeout, user_data, time_sent)  # 接收ping回复

    sock.close()  # 关闭套接字
    return delay


# Ping函数，进行多次ping并统计结果
def ping(dest_addr, timeout=1, count=4, user_data="Ping"):
    """
    对目标主机进行多次ping操作，并显示统计结果。

    :param dest_addr: 目标主机地址
    :param timeout: 每次ping的超时时间
    :param count: 发送ping请求的次数
    :param user_data: 用户自定义的字符串，将作为数据部分发送
    :return: None
    """
    try:
        # 将主机名解析为IP地址
        dest_ip = socket.gethostbyname(dest_addr)
        source_ip = socket.gethostbyname(socket.gethostname())

        print(f"\n----- Pinging {dest_ip} from {source_ip} with {len(user_data)} bytes of data -----")

        rtt_list = []  # 用于存储每次ping的往返时间
        for i in range(count):
            print(f"\n------------Ping {i + 1} --------------")
            delay = do_one_ping(dest_ip, timeout, user_data)
            if delay is None:
                print("请求超时。")  # 超时未收到响应
            else:
                print(f"来自 {dest_ip} 的回复：时间={delay:.3f}ms")
                rtt_list.append(delay)
            time.sleep(1)  # 每次ping之间暂停1秒

        if rtt_list:
            # 输出统计结果，包括最小、最大、平均RTT和丢包率
            print(f'\n-----------------------------------------所有的ping结束-------------------------------------')
            print(f"\n--- {dest_addr} ping 统计 ---")
            print(
                f"{count} 个数据包已发送，{len(rtt_list)} 个收到回复，丢失率 {((count - len(rtt_list)) / count) * 100:.1f}%")
            print(f"往返时间最小/平均/最大:\n"
                  f"{min(rtt_list):.3f} ms\n"
                  f"{sum(rtt_list) / len(rtt_list):.3f} ms\n"
                  f"{max(rtt_list):.3f} ms")
        else:
            print(f"\n--- {dest_addr} ping 统计 ---")
            print(f"没有收到任何回复。")

    except socket.gaierror:
        print(f"无法解析主机 {dest_addr}。请检查地址后重试。")


def ping_multiple_addresses(addresses, timeout=1, count=4):
    """
    并行ping多个地址，交替输出ping结果。
    """
    threads = []

    for addr in addresses:
        thread = threading.Thread(target=ping, args=(addr, timeout, count))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


# 使用 argparse 解析命令行参数
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ICMP Ping工具 - 测量网络延迟")
    parser.add_argument('--hosts', nargs='+', required=True, help="目标主机名或IP地址列表")
    parser.add_argument('--timeout', type=int, default=1, help="每次ping的超时时间，默认1秒")
    parser.add_argument('--count', type=int, default=4, help="发送ping的次数，默认4次")
    parser.add_argument('--data', type=str, default="Ping", help="自定义传输的数据")
# python ping.py --hosts lancaster.ac.uk cctv.com.cn --timeout 2 --count 2 --data 'Hello world'
    args = parser.parse_args()

    # 传递用户输入的参数给 ping 函数
    # ping(args.host, args.timeout, args.count, args.data)
    ping_multiple_addresses(args.hosts, args.timeout, args.count)
