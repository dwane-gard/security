import socket
import collections
import optparse

def flatten_list(ze_list):
    for sublist in ze_list:
        if isinstance(sublist, collections.Iterable) and not isinstance(sublist, (str, bytes)):
            yield from flatten_list(sublist)
        else:
            yield sublist


class Client:
    def __init__(self, discovery, request):
        self.ip = b'192.168.10.1'
        print(self.ip)
        self.port = 67

        if discovery is True:
            self.type = 0
        elif request is True:
            self.type = 1
        else:
            print('[!] Packet type not defined use the argument -d or -r')
            exit(1)

        self.dhcp_packet = self.craft_packet()

    def craft_packet(self):
        op = [b'\x01']  # REquest=ff or reply=00
        htype = [b'\x01']  # Hardware address type 01=ethernet
        hlen = [b'\x06']  # Hardware length
        hops = [b'\x00']  # hops; number of relay agents the message travels through, each one will add one
        xid = [b'\x00', b'\x00', b'\x17', b'\x3d']  # Transaction ID a random number chosen by the client to identify an ip address allocation
        secs = [b'\x00']*2  # number of seconds elapsed since clent sent a dhcp request
        flags = [b'\x00']*2  # leftmost bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
        ciaddr = [b'\x00']*4  # client ip address
        yiaddr = [b'\x00']*4  # 'your' ip address, as assigned by server
        siaddr = [b'\x00']*4  # Server ip address

        giaddr = [b'\x00']*4  # first relay agent ip address
        chaddr = [b'\x08', b'\x00', b'\x27', b'\x94', b'\xf3', b'\x82']  # client hardware address
        chaddr_padding = [b'\x00']*(16-len(chaddr))
        sname = [b'\x00']*64  # server host name
        file = [b'\x00']*128  # bootfile name, routing information defined by server to the client
        magic_cookie = [b'\x63', b'\x82', b'\x53', b'\x63']
        options = [b'\x35', b'\x01', b'\x01',  # DHCP, len, Offer
                   b'\x3d', b'\x07', b'\x01', chaddr, # client id
                   b'\x37', b'\x04', b'\x01', b'\x03', b'\x06', b'\x2a',
                   b'\xff',  # end flag
                   # padding to end at word boundry for the options
                   ]
        if self.type == 0:
            options[2] = b'\x01'
        elif self.type == 1:
            options[2] = b'\x03'

        options = list(flatten_list(options))

        options_padding_check = len(options)
        options_padding_length = 0
        while (options_padding_check / 4) != int(options_padding_check / 4):
            options_padding_check += 1
            options_padding_length += 1

        print(options_padding_length / 4)
        if options_padding_length > 1:
            options_padding = [[b'\x00'] * (options_padding_length - 1), [b'\x0a']]
            options_padding = list(flatten_list(options_padding))

            return_packet = [op, htype, hlen, hops, xid, secs, flags, ciaddr, yiaddr, siaddr, giaddr, chaddr,chaddr_padding, sname,
                             file, magic_cookie, options, options_padding]

        else:
            return_packet = [op, htype, hlen, hops, xid, secs, flags, ciaddr, yiaddr, siaddr, giaddr, chaddr, chaddr_padding, sname,
                             file, magic_cookie, options]

        return_packet = [item for sublist in return_packet for item in sublist]
        print(return_packet)
        return_packet = b''.join(return_packet)

        return_packet = bytearray(return_packet)

        return return_packet

    def start_sockets(self):
        self.dhcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dhcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def start(self):
        self.dhcp_socket.sendto(self.dhcp_packet, ('255.255.255.255', 67))

    def test(self):
        print(self.dhcp_packet)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-d', action='store_true', default=False, help='Send discovery dhcp packet')
    parser.add_option('-r', action='store_true', default=False, help='Send discovery request packet')

    options, args = parser.parse_args()

    discovery = options.d
    request = options.r

    client = Client(discovery, request)
    client.test()
    client.start_sockets()
    client.start()

