import socket
import select
import optparse

class ZeScanner:
    def __init__(self, ip, port, type):
        self.ip = ip
        self.port = port
        self.type = type
        pass
    def start_tcp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO)

        s.connect(self.ip)
        s.send()
    def start_udp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SOCK_RAW)




if __name__ == '__main__':
    scan = ZeScanner(('192.168.1.1'), 80)
