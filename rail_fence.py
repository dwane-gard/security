import collections
import itertools
import time

def fence(cipher_text, key_size):
    '''
    used by decode for its processing
    :param cipher_text:
    :param key_size:
    :return:
    '''
    # Create a list of lists with null values to be filled
    fence = [[None] * len(cipher_text) for n in range(key_size)]

    # Discover the pattern of the zig zag
    acending_order = range(key_size - 1)
    decending_order = range(key_size - 1, 0, -1)
    # for each in zip(acending_order, decending_order):
    #     print(each)
    rails = list(acending_order) + list(decending_order)

    # Find the position of each letter in the rails
    for position, letter in enumerate(cipher_text):
        fence[rails[position % len(rails)]][position] = letter

    if 0: # debug
        for rail in fence:
            print(''.join('.' if x is None else str(x) for x in rail))

    # If the entry is not none add it to the list to be returned
    return [x for rail in fence for x in rail if x is not None]

def encode(text, n):
    '''
    Encode text using a railfence cipher with a key of n length
    :param text:
    :param n:
    :return:
    '''
    return ''.join(fence(text, n))

def decode(text, n):
    '''
    decode text using a railfence cipher with a key of n length
    :param text:
    :param n:
    :return:
    '''
    rng = range(len(text))
    pos = fence(rng, n)
    return ''.join(text[pos.index(n)] for n in rng)


if __name__ == '__main__':
    # 10 chars dontattack
    # z = encode('DONTATTACKDONTATTACKDONTATTACKDONTATTACKDONTATTACKDONTATTACKDONTATTACKDONTATTACKDONTATTACK', 10)
    # print(z) # ACTWTAKA.ANT.D
    # print(z)
    # y = decode(z, 10)
    # print(y)
    for x in range(2, 500, 1):
        print('\n')
        print(x)


        cipher_text = "S_   ltes e__owesft4ya'h r_ernadinhohn_hstfeamion coo iost  lhrooidskeutsio t,aPeeut_eemlc tmkhegi_wschoool31neOen Cbale4h s tee_  oi_r yjnsr  iat_.>dslu}4 nd asthsnCg\  it_ Misdirection_tCaeesa Oe1elr__firiOR_lelsmk_hlabsfkabM{fbbliuec_p  eiecn P1oaubco a_ite_headm34rebihchtHo4c"

        # for each in range(1,28,1):
        # fraction = (int(len(cipher_text)/2))
        # cipher_text = cipher_text[:fraction], cipher_text[fraction:]
        # print(collections.Counter(cipher_text))
        # for each_cipher_text in cipher_text:
        y = decode(cipher_text, x)
        # print(y)
        if '3441' in y:
            print(y)
            time.sleep(10)
        #     print(y) # ATTACK.AT.DAWN\


