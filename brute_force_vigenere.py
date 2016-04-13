# from co_incidence_index import CheckIC

import co_incidence_index
from queue import Queue
import threading

class Answers:
    def __init__(self, ze_ic, ze_key, plain_text, E, A, T):
        self.ic = ze_ic
        self.key = ze_key
        self.plain_text = plain_text
        self.E = E
        self.A = A
        self.T = T



f = open('sowpods.txt', 'r').readlines()
cipher_text = 'WJHZR DIAKZ TMCYS OMLVY HISNF BNZRP' \
              'OESFJ RVLWL MIPOA LJAKD SQWLH KYSCN' \
              'RMHPB OQNQQ MNBXC CACJN BOVVT LAUWJ' \
              'RNISI FFBJO WZWIV NCWQM AUEEX TNOMR' \
              'JIIYH ISNWD Y'
debug_flag = 0
cipher_text = cipher_text.replace(" ", '')
cipher_text = cipher_text.replace("\n", '')

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z']
count = 0
possible_answers = []


def run(each_line):
    print('[threads active] %s ' % threading.active_count())

    key = each_line.replace(' ', '')
    key = [x for x in key]
    key_size = len(key) - 1

    cipher_list_sized = [cipher_text[i:i+key_size] for i in range(0, len(cipher_text), key_size)]

    deciphered_message = ''
    for each_part in cipher_list_sized:
        # print(each_part)
        x = 0
        for each_char in key:
            try:
                if each_char == '\n':
                    continue

                key_letter = alphabet.index(each_char.upper())
                cypher_letter = alphabet.index(each_part[x].upper())

                if cypher_letter > key_letter:
                    deciphered_letter_index = cypher_letter - key_letter

                elif key_letter > cypher_letter:
                    deciphered_letter_index = key_letter - cypher_letter
                elif key_letter == cypher_letter:
                    deciphered_letter_index = key_letter - cypher_letter
                else:
                    print(key_letter, cypher_letter)
                    deciphered_letter_index = 0
                    exit()

                if debug_flag == 1:
                    print('[cypher letter] %s | %s' % (str(alphabet[cypher_letter]), str(cypher_letter)))
                    print('[key letter] %s | %s' % (str(each_char.upper()), str(key_letter)))
                    # print('[shift] %s' % str(deciphered_letter))
                    print('[new letter] %s | %s' % (str(alphabet[deciphered_letter_index]), str(deciphered_letter_index)))
                deciphered_letter = alphabet[deciphered_letter_index]
                deciphered_message += deciphered_letter
                x += 1
            except Exception:
                pass

    checkIC = co_incidence_index.CheckIC(deciphered_message)
    ic = checkIC.ic
    E = checkIC.E
    A = checkIC.A
    T = checkIC.T
    X = checkIC.X
    J = checkIC.J
    Z = checkIC.Z


    #derp
    # if ic > 0.06:
    #
    #     if E > 0.09 and A > 0.04 and T > 0.03:
    #         if Z < 0.02 or J < 0.02 or X < 0.02:
    for each_word in f:
        if each_word.upper() in deciphered_message:
            print(E, A, T)
            print(Z, J, X)
            # possible_answers.append(Answers(ic, each_line, deciphered_message, E, A, T))
            print('\n'*2)
            print(each_line)
            print(deciphered_message)
            print(ic)
        pass

        # exit()

    else:

        # print(cipher_text)
        # print(deciphered_message)
        # print(each_line)
        # print(ic)
        # if count == 10:
        #     exit()
        pass
    # count += 1


max_threads = 3
threads = []
for each_line in f:
    for i in range(max_threads):
        worker = threading.Thread(target=run, args=(each_line,))
        worker.setDaemon(True)
        threads.append(worker)
        worker.start()



    # run(each_line)




