# from co_incidence_index import CheckIC

import co_incidence_index
from queue import Queue
import multiprocessing

lock = multiprocessing.Lock()

class Answers:
    def __init__(self, ze_ic, ze_key, plain_text, E, A, T):
        self.ic = ze_ic
        self.key = ze_key
        self.plain_text = plain_text
        self.E = E
        self.A = A
        self.T = T




f = open('sowpods1.txt', 'r').readlines()
cipher_text = 'WJHZR DIAKZ TMCYS OMLVY HISNF BNZRP' \
              'OESFJ RVLWL MIPOA LJAKD SQWLH KYSCN' \
              'RMHPB OQNQQ MNBXC CACJN BOVVT LAUWJ' \
              'RNISI FFBJO WZWIV NCWQM AUEEX TNOMR' \
              'JIIYH ISNWD Y'

# test_cipher_text = 'ALTDW ZENJD OIC' # This is a cypher
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
    # print(key)
    # print(len(key))
    key_size = len(key)


    cipher_list_sized = [cipher_text[i:i+key_size] for i in range(0, len(cipher_text), key_size)]
    # print(str(cipher_list_sized) + '|' +cipher_text + '|' + str(len(key)))

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
                # print(deciphered_message)


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

    # if E > 0.8 and A > 0.03 and T > 0.02:
    word_count = 0
    word_list = []
    if 'CYPHER' in deciphered_message:
        lock.acquire()
        print('+'*20)
        print(deciphered_message)
        print(E, A, T)
        print(Z, J, X)
        # possible_answers.append(Answers(ic, each_line, deciphered_message, E, A, T))
        print(each_line)
        print(key)
        print(ic)
        lock.release()

    if Z < 0.02 and J < 0.02 and X < 0.02:
        for each_word in f:

            each_word = each_word.strip('\n').upper()
            if len(each_word) == 2:
                pass
            elif len(each_word) == 3:
                pass
            else:
                if each_word in deciphered_message:
                    word_count += 1
                    word_list.append(each_word)
                    # lock.acquire()
                    # print(each_word)
                    # lock.release()
    if word_count > 4:
        lock.acquire()
        print('+'*20)
        print(word_list)
        print(deciphered_message)
        print(E, A, T)
        print(Z, J, X)
        # possible_answers.append(Answers(ic, each_line, deciphered_message, E, A, T))
        print(each_line)
        print(key)
        print(ic)
        lock.release()





def create_brute():
    brute = []
    brute.append('HELLO')
    # 1 char
    for each in range(0, 26, 1):
        try:
            (alphabet[each])
        except:
            print(alphabet[each])

    # 2 Characters
    for each in range(0, 26, 1):
        print(alphabet[each]+ str(2))
        for each1 in range(0, 26, 1):
            brute.append(alphabet[each] + alphabet[each1])

    # 3 Characters
    for each in range(0, 26, 1):
        print(alphabet[each] + str(3))
        for each1 in range(0, 26, 1):
            for each2 in range(0, 26, 1):
                brute.append(alphabet[each] + alphabet[each1] + alphabet[each2])

    # 4 Characters
    for each in range(0, 26, 1):
        print(alphabet[each] + str(4))
        for each1 in range(0, 26, 1):
            for each2 in range(0, 26, 1):
                for each3 in range(0, 26, 1):
                    brute.append(alphabet[each] + alphabet[each1] + alphabet[each2] + alphabet[each3])
    # 5 Characters
    for each in range(0, 26, 1):
        print(alphabet[each] + str(5))
        for each1 in range(0, 26, 1):
            for each2 in range(0, 26, 1):
                for each3 in range(0, 26, 1):
                    for each4 in range(0, 26, 1):
                        brute.append(alphabet[each] + alphabet[each1] + alphabet[each2] + alphabet[each3] + alphabet[each4])

    # 6 Characters
    # for each in range(0, 25, 1):
    #     print(alphabet[each] + str(6))
    #     for each1 in range(0, 25, 1):
    #         for each2 in range(0, 25, 1):
    #             for each3 in range(0, 25, 1):
    #                 for each4 in range(0, 25, 1):
    #                     for each5 in range (0, 25, 1):
    #                         brute.append(alphabet[each] + alphabet[each1] + alphabet[each2] + alphabet[each3] + alphabet[each4] + alphabet[each5])


    # 7 Characters
    # for each in range(0, 25, 1):
    #     print(alphabet[each] + str(7))
    #     for each1 in range(0, 25, 1):
    #         for each2 in range(0, 25, 1):
    #             for each3 in range(0, 25, 1):
    #                 for each4 in range(0, 25, 1):
    #                     for each5 in range (0, 25, 1):
    #                         for each6 in range(0,25,1):
    #                         brute.append(alphabet[each] + alphabet[each1] + alphabet[each2] + alphabet[each3] + alphabet[each4] + alphabet[each5]+ alphabet[each6])

    # 8 characters
    # for each in range(0, 25, 1):
    #     print(alphabet[each] + str(8))
    #     for each1 in range(0, 25, 1):
    #         for each2 in range(0, 25, 1):
    #             for each3 in range(0, 25, 1):
    #                 for each4 in range(0, 25, 1):
    #                     for each5 in range (0, 25, 1):
    #                         for each6 in range(0,25,1):
    #                             for each7 in range(0,25,1):
    #                                 brute.append(alphabet[each] + alphabet[each1] + alphabet[each2] + alphabet[each3] + alphabet[each4] + alphabet[each5]+ alphabet[each6] + alphabet[each7])
    return brute


def worker(inq):
    run(inq)

if __name__ == '__main__':
    brute = create_brute()

    m = multiprocessing.Manager()
    ze_pool = multiprocessing.Pool(4)
    ze_pool.map(worker, brute)

    # for each in brute:
    #     # ze_queue.put(each)
    #     run(each)

    # for each in f:
    #     ze_queue.put(each)

    # p.start()
    # p.join()



#
#
#
#
