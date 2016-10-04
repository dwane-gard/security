import socket
import select
import optparse
import os
import time
from Crypto.Util.number import getStrongPrime, getRandomInteger

def get_random(size):
    # Get (size) amount of random bytes
    rand = os.urandom(size)
    # Covert bytes to a integer
    output = int.from_bytes(rand, byteorder='big')
    return output


class Alpha:
    '''
    This Class is an example of the diffie-hellman handshake.
    It broadcasts on port UDP 101 and receives on UDP port 100.
    It Broadcasts a P and G number which are generated randomly. It will then broad cast a mod of a secret generated
    from these numbers.

    It then receives the mod of a secret Beta will generate.
    Using Alpha's own secret, the P number and Beta's mod of secret a shared secret is generated which can be
    used in future communication
    '''
    def __init__(self, p, g, a, verbose):
        self.verbose = verbose
        self.alpha_secret = a

        self.alpha_mod_secret = 0
        self.mod_beta_secret = 0

        self.shared_secret = 0
        self.p = p
        self.g = g

        # Configure the socket to listen of UDP
        self.ze_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def exchange(self):
        # Configure the socket for broadcasting
        self.ze_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Configure the socket to listen on port 100
        self.ze_socket.bind(('', 100))

        # Create the mod of Alpha's secret
        self.alpha_mod_secret = (g ** self.alpha_secret) % p

        print('[+] Ready to receive')

        # self.ze_socket.sendto((b'thisisapandg|%d|%d' % (self.p, self.g)), ('255.255.255.255', 101))

        # If shared secret is not yet computed be ready to receive data
        while self.shared_secret == 0:
            r, w, x = select.select([self.ze_socket], [0], [])
            for each in r:
                frame, void = each.recvfrom(10000)
                if self.verbose is True:
                    print('[+] Recieved Something! from %s' % void[0])

                if frame.startswith(b'iamready'):
                    if self.verbose is True:
                        print('[+] %s is ready to start the exchange' % void[0])

                    # Broadcast the P and G numbers
                    if self.verbose is True:
                        print('[+] Broadcasting the P and G numbers')
                    self.ze_socket.sendto((b'thisisapandg|%d|%d' % (self.p, self.g)), ('255.255.255.255', 101))

                # Receive the mod of Beta's secret
                if frame.startswith(b'thisisabetamodsecret'):
                    null, self.mod_beta_secret = frame.split(b'|')

                    # Broadcast the mod of Alpha's secret
                    if self.verbose is True:
                        print("[+] Broadcasting the mod of Alpha's secret")
                    self.ze_socket.sendto(b'thisisalphamodsecret|%d' % self.alpha_mod_secret, ('255.255.255.255', 101))

                    ready = True

                # Check that the mod of Beta's secret has been received
                if self.mod_beta_secret != 0:
                    self.mod_beta_secret = int(self.mod_beta_secret)

                    # Create the shared secret using Beta and Alphas mod of their secrets
                    self.shared_secret = (self.mod_beta_secret ** self.alpha_secret) % self.p

    def output(self):
        print('''|------------||   Output   ||------------|''')
        print('[p] %d' % self.p)
        print('[g] %d' % self.g)
        print('[alpha mod secret] %d' % self.alpha_mod_secret)
        print('[alpha secret] %d' % self.alpha_secret)
        print('[mod beta secret] %d' % self.mod_beta_secret)
        print('[shared key] %d' % self.shared_secret)
        print('''|-----------------------------------------|''')

class Beta:
    '''
    This Class is an example of the diffie-hellman handshake.
    It broadcasts on UDP port 100 and receives on UDP port 101.
    It receives P and G from Alpha and then broadcasts the mod of a secret it generates.
    After receiving the mod of the secret Alpha generates they both generate the same shared secret which can be
    used in future communication
    '''
    def __init__(self, b, verbose):
        self.verbose = verbose
        self.beta_secret = b
        self.p = 0
        self.g = 0
        self.mod_beta_secret = 0
        self.shared_secret = 0
        self.alpha_mod_secret = 0

        # Configure the socket to listen on UDP
        self.ze_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def exchange(self):
        # Configure the socket to broadcast
        self.ze_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Configure the socket to listen on port 101
        self.ze_socket.bind(('', 101))

        self.ze_socket.sendto(b'iamready', ('255.255.255.255', 100))

        # If shared secret is not yet computed be ready to recieve data
        while self.shared_secret == 0:
            r, w, x = select.select([self.ze_socket], [], [])

            for each in r:
                frame, void = each.recvfrom(10000)

                if self.verbose is True:
                    print('[+] Recieved Something from %s' % void[0])

                # print(frame)

                # Get the P and G numbers from Alpha
                if frame.startswith(b'thisisapandg'):
                    null, p, g = frame.split(b'|')
                    self.p = int(p)
                    self.g = int(g)

                    # Create a mod of Beta secret
                    self.mod_beta_secret = (self.g**self.beta_secret) % self.p

                    # Send Alpha the mod of Betas secret
                    if self.verbose is True:
                        print("[+] Broadcasting the mod of Beta's secret")
                    self.ze_socket.sendto(b'thisisabetamodsecret|%d' % self.mod_beta_secret, ('255.255.255.255', 100))

                # Get the mod of Alpha's secret
                if frame.startswith(b'thisisalphamodsecret'):
                    null, self.alpha_mod_secret = frame.split(b'|')
                    self.alpha_mod_secret = int(self.alpha_mod_secret)

                # Check that the mod of Alpha's secret has been recieved
                if self.alpha_mod_secret != 0:

                    # Create the shared secret using Beta and Alphas mod of their secrets
                    self.shared_secret = (self.alpha_mod_secret**self.beta_secret) % self.p

    def output(self):
        print('''|------------||   Output   ||------------|''')
        print('[p] %d' % self.p)
        print('[g] %d' % self.g)
        print('[alpha mod secret] %d' % self.alpha_mod_secret)
        print('[beta secret] %d' % self.beta_secret)
        print('[mod beta secret] %d' % self.mod_beta_secret)
        print('[shared key] %d' % self.shared_secret)
        print('''|-----------------------------------------|''')

if __name__ == '__main__':
    usage = ' usage: %prog [-a|-b] -s <>'
    desc = 'This Python script is an example of how the Diffie-Hellman handshake works. The Alpha instance is' \
           ' required to be ran first and both require admin privileges.'
    parser = optparse.OptionParser(usage=usage, description=desc)
    parser.add_option('-a', '--alpha', action='store_true', default=False, help='Set client as alpha.')
    parser.add_option('-b', '--beta', action='store_true', default=False, help='Set client as beta.')
    parser.add_option('-v', '--verbose', action='store_true', default=False, help='Print status.')
    parser.add_option('-s', '--size', dest='size', default=2, help='Set how many bytes long the keys will be,'
                                                                   ' [default=2]')
    options, args = parser.parse_args()
    alpha_tog = options.alpha
    beta_tog = options.beta
    verbose = options.verbose
    size = int(options.size)

    if alpha_tog is True and beta_tog is True:
        print("[!] Error: can't set both alpha and beta use one per instance")
        exit(1)
    try:
        if alpha_tog is True:
            # a = getRandomInteger(512)
            a = get_random(size)
            p = getStrongPrime(512)
            g = getStrongPrime(512)
            alpha = Alpha(p, g, a, verbose)
            alpha.exchange()
            alpha.output()
            exit()
        elif beta_tog is True:
            b = get_random(size)
            # b = getRandomInteger(512)
            beta = Beta(b, verbose)
            beta.exchange()
            beta.output()
            exit()
    except PermissionError:
        print("[!] Error: you must have sudo permissions in order to broadcast")
        exit(1)






