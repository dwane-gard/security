import math
import socket
import select
import optparse


class Mod:
    def __init__(self, a1, a2, b):
        a = a1 **a2
        x = a / b
        y = x - int(x)
        self.answer = int(round(y * b))
        print('A = %d ** %d mod %d = %d' % (a1, a2, b, self.answer))


class Alpha:
    def __init__(self, p, g, a):
        self.alpa_secret = a
        self.alpa_mod_secret = Mod(g, a, p).answer
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

                    self.shared_secret = Mod(self.mod_beta_secret, self.alpa_secret, self.p).answer
                    print('[p] %x' % self.p)
                    print('[g] %x' % self.g)
                    print('[alpha mod secret] %x' % self.alpa_mod_secret)
                    print('[alpha secret] %x' % self.alpa_secret)
                    print('[mod beta secret] %x' % self.mod_beta_secret)
                    print('[shared key] %x' % self.shared_secret)
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
                    self.mod_beta_secret = Mod(self.g, self.beta_secret, self.p).answer

                    self.ze_socket.sendto(b'thisisabetamodsecret|%d' % self.mod_beta_secret, ('255.255.255.255', 100))

                if frame.startswith(b'thisisalphamodsecret'):
                    null, self.alpha_mod_secret = frame.split(b'|')
                    self.alpha_mod_secret = int(self.alpha_mod_secret)
                if self.alpha_mod_secret != 0:
                    self.shared_secret = Mod(self.alpha_mod_secret, self.beta_secret, self.p).answer
                    print('[p] %x' % self.p)
                    print('[g] %x' % self.g)
                    print('[alpha mod secret] %x' % self.alpha_mod_secret)
                    print('[beta secret] %d' % self.beta_secret)
                    print('[mod beta secret] %x' % self.mod_beta_secret)
                    print('[shared key] %x' % self.shared_secret)
                    exit()


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-a', action='store_true', default=False, help='set client as alpha')
    parser.add_option('-b', action='store_true', default=False, help='set client as beta')

    options, args = parser.parse_args()

    alpha_tog = options.a
    beta_tog = options.b

    if alpha_tog is True:
        a = 6
        p = 23
        g = 5
        alpha = Alpha(p, g, a)
        alpha.exchange()

    elif beta_tog is True:
        b = 15
        beta = Beta(b)
        beta.exchange()






