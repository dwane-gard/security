import optparse
from Crypto.Util.number import getStrongPrime, getRandomInteger
from diffie_hellman import Alpha, Beta

if __name__ == '__main__':
    usage = ' usage: %prog [-a|-b] -s <>'
    desc = 'This Python script is an example of how the Diffie-Hellman handshake works. The Alpha instance is' \
           ' required to be ran first and both require admin privileges.'
    parser = optparse.OptionParser(usage=usage, description=desc)
    parser.add_option('-a', '--alpha', action='store_true', default=False, help='Set client as alpha.')
    parser.add_option('-b', '--beta', action='store_true', default=False, help='Set client as beta.')
    parser.add_option('-v', '--verbose', action='store_true', default=False, help='Print status.')
    parser.add_option('-s', '--size', dest='size', default=2048, help='Set how many bits long the prime and base'
                                                                      ' numbers will be, [default=2048]')
    parser.add_option('-e', '--secret', dest='secret', default=512, help='Set how many bits long the secret number will'
                                                                         ' be [default=512]')
    options, args = parser.parse_args()
    alpha_tog = options.alpha
    beta_tog = options.beta
    verbose = options.verbose
    size = int(options.size)
    secret = int(options.secret)

    if alpha_tog is True and beta_tog is True:
        print("[!] Error: can't set both alpha and beta use one per instance")
        exit(1)
    try:
        if alpha_tog is True:
            a = getRandomInteger(secret) # This needs to be large, at least 512bit
            p = getStrongPrime(size)
            g = getStrongPrime(size)

            alpha = Alpha(p, g, a, verbose)
            alpha.exchange()
            alpha.output()
            exit()
        elif beta_tog is True:
            # b = get_random(size)
            b = getRandomInteger(secret) # This needs to be large, at least 512bit
            beta = Beta(b, verbose)
            beta.exchange()
            beta.output()
            exit()
    except PermissionError:
        print("[!] Error: you must have sudo permissions in order to broadcast")
        exit(1)
