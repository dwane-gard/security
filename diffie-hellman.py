import math
import socket
import select
import optparse
import time
import os

def get_random(size):
    rand = os.urandom(size)
    output = int.from_bytes(rand, byteorder='big')
    return output

class Mod:
    ''' Cant be used for alrge number due to python constrains on floats'''
    def __init__(self, a1, a2, b):
        a = a1 ** a2
        # print(a)
        x = a / b
        print(x)
        y = x - int(x)
        print(y)
        self.answer = int(round(y * b))
    # def print_answer:
        print('A = %d ** %d mod %d = %d' % (a1, a2, b, self.answer))


class Alpha:
    def __init__(self, p, g, a):
        self.alpa_secret = a
        # self.alpa_mod_secret = Mod(g, a, p).answer
        self.alpa_mod_secret = (g**self.alpa_secret) % p
        self.mod_beta_secret = 0

        self.shared_secret = 0
        self.p = p
        self.g = g
        self.ze_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def exchange(self):
        self.ze_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.ze_socket.bind(('', 100))

        self.ze_socket.sendto((b'thisisapandg|%d|%d' % (self.p, self.g)), ('255.255.255.255', 101))
        while True:
            r, w, x = select.select([self.ze_socket], [], [])

            for each in r:
                print('Recieved Something!')
                frame, void = each.recvfrom(10000)
                print(void)
                print(frame)

                if frame.startswith(b'thisisabetamodsecret'):
                    null, self.mod_beta_secret = frame.split(b'|')

                    self.ze_socket.sendto(b'thisisalphamodsecret|%d' % self.alpa_mod_secret, ('255.255.255.255', 101))

                if self.mod_beta_secret != 0:

                    self.mod_beta_secret = int(self.mod_beta_secret)

                    # self.shared_secret = Mod(self.mod_beta_secret, self.alpa_secret, self.p).answer
                    self.shared_secret = (self.mod_beta_secret**self.alpa_secret) % self.p
                    print('[p] %d' % self.p)
                    print('[g] %d' % self.g)
                    print('[alpha mod secret] %d' % self.alpa_mod_secret)
                    print('[alpha secret] %d' % self.alpa_secret)
                    print('[mod beta secret] %d' % self.mod_beta_secret)
                    print('[shared key] %d' % self.shared_secret)
                    exit()


class Beta:
    def __init__(self, b):
        self.beta_secret = b
        self.p = 0
        self.g = 0
        self.mod_beta_secret = 0
        self.shared_secret = 0
        self.ze_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.alpha_mod_secret = 0

    def exchange(self):
        self.ze_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.ze_socket.bind(('', 101))

        while True:
            r, w, x = select.select([self.ze_socket], [], [])
            for each in r:
                print('Recieved Something!')
                frame, void = each.recvfrom(10000)
                print(frame)
                if frame.startswith(b'thisisapandg'):
                    null, p, g = frame.split(b'|')
                    self.p = int(p)
                    self.g = int(g)
                    # self.mod_beta_secret = Mod(self.g, self.beta_secret, self.p).answer
                    self.mod_beta_secret = (self.g**self.beta_secret) % self.p

                    self.ze_socket.sendto(b'thisisabetamodsecret|%d' % self.mod_beta_secret, ('255.255.255.255', 100))

                if frame.startswith(b'thisisalphamodsecret'):
                    null, self.alpha_mod_secret = frame.split(b'|')
                    self.alpha_mod_secret = int(self.alpha_mod_secret)
                if self.alpha_mod_secret != 0:
                    # self.shared_secret = Mod(self.alpha_mod_secret, self.beta_secret, self.p).answer
                    self.shared_secret = (self.alpha_mod_secret**self.beta_secret) % self.p

                    print('[p] %d' % self.p)
                    print('[g] %d' % self.g)
                    print('[alpha mod secret] %d' % self.alpha_mod_secret)
                    print('[beta secret] %d' % self.beta_secret)
                    print('[mod beta secret] %d' % self.mod_beta_secret)
                    print('[shared key] %d' % self.shared_secret)
                    exit()


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-a', action='store_true', default=False, help='set client as alpha')
    parser.add_option('-b', action='store_true', default=False, help='set client as beta')

    options, args = parser.parse_args()

    alpha_tog = options.a
    beta_tog = options.b

    # any number larger then 2 bytes is too large to be workable
    size = 2

    if alpha_tog is True:

        a = get_random(size+1)
        # a = 6
        p = get_random(size)
        # p = 23
        g = get_random(size)
        # g = 5
        alpha = Alpha(p, g, a)
        alpha.exchange()

    elif beta_tog is True:
        b = get_random(size+1)
        # b = 15
        beta = Beta(b)
        beta.exchange()






