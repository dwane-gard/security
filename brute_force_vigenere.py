# from co_incidence_index import CheckIC

import co_incidence_index
from queue import Queue
import multiprocessing

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

# test_cipher_text = 'ALTDW ZENJD oiC'
# cipher_text = test_cipher_text
debug_flag = 0
cipher_text = cipher_text.replace(" ", '')
cipher_text = cipher_text.replace("\n", '')

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z']
count = 0
possible_answers = []


def run(each_line):
    # print('[threads active] %s ' % threading.active_count())

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


                deciphered_letter_index = cypher_letter - key_letter

                # if deciphered_letter_index > 0:
                #     deciphered_letter_index += 26

                # else:
                #     print(key_letter, cypher_letter)
                #     deciphered_letter_index = 0
                #     exit()

                if debug_flag == 1:
                    print('[cypher letter] %s | %s' % (str(alphabet[cypher_letter]), str(cypher_letter)))

                    print('[key letter] %s | %s' % (str(each_char.upper()), str(key_letter)))
                    # print('[shift] %s' % str(deciphered_letter))
                    print('[new letter] %s | %s' % (str(alphabet[deciphered_letter_index]), str(deciphered_letter_index)))
                    print('\n')
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
    #     if E > 0.1 and A > 0.05 and T > 0.04:
    #         if Z < 0.02 and J < 0.02 and X < 0.02:
    # if ic > 0.05:
    word_count = 0
    if ic > 0.05:
        for each_word in f:

            each_word = each_word.strip('\n').upper()
            if len(each_word) == 2:
                continue
            if len(each_word) == 3:
                continue
            if each_word in deciphered_message:
                word_count += 1
                print(each_word)
            if word_count > 3:
                print(deciphered_message)
                print(E, A, T)
                print(Z, J, X)
                # possible_answers.append(Answers(ic, each_line, deciphered_message, E, A, T))
                print('+'*20)
                print(each_line)
                print(each_word)
                print(ic)
                break
                # exit()




    # else:
        # print(ic)
        # print(cipher_text)
        # print(deciphered_message)
        # print(each_line)
        # print(ic)
        # if count == 10:
        #     exit()
        # pass
    # count += 1


# max_threads = 3
# threads = []
# for each_line in f:
#     run(each_line)
#
def create_brute():
    brute = []
    for each in range(0, 25, 1):
        try:
            (alphabet[each])
        except:
            print(alphabet[each])
    for each in range(0, 25, 1):
        print(alphabet[each]+ str(2))
        for each1 in range(0, 25, 1):
            brute.append(run(alphabet[each] + alphabet[each1]))

    for each in range(0, 25, 1):
        print(alphabet[each] + str(3))
        for each1 in range(0, 25, 1):
            for each2 in range(0, 25, 1):
                brute.append(alphabet[each] + alphabet[each1] + alphabet[each2])
    for each in range(0, 25, 1):
        print(alphabet[each] + str(4))
        for each1 in range(0, 25, 1):
            for each2 in range(0, 25, 1):
                for each3 in range(0, 25, 1):

                    brute.append(alphabet[each] + alphabet[each1] + alphabet[each2] + alphabet[each3])
    for each in range(0, 25, 1):
        print(alphabet[each] + str(5))
        for each1 in range(0, 25, 1):
            for each2 in range(0, 25, 1):
                for each3 in range(0, 25, 1):
                    for each4 in range(0, 25, 1):
                        brute.append(alphabet[each] + alphabet[each1] + alphabet[each2] + alphabet[each3] + alphabet[each4])

    for each in range(0, 25, 1):
        print(alphabet[each] + str(5))
        for each1 in range(0, 25, 1):
            for each2 in range(0, 25, 1):
                for each3 in range(0, 25, 1):
                    for each4 in range(0, 25, 1):
                        for each5 in range (0, 25, 1):
                            brute.append(alphabet[each] + alphabet[each1] + alphabet[each2] + alphabet[each3] + alphabet[each4] + alphabet[each5])
    return brute


def worker(inq):
    while True:
        obj = inq.get()
        print(obj)
        run(obj)

if __name__ == '__main__':
    max_threads = 3
    ze_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=worker, args=(ze_queue,))
    brute = create_brute()
    for each in brute:
        ze_queue.put(each)

    for each in f:
        ze_queue.put(each)

    p.start()
    p.join()



#
#
#
#
