# from co_incidence_index import CheckIC

import co_incidence_index
import kasiski
import multiprocessing
import itertools

lock = multiprocessing.Lock()
# 0 = Brute 1 = dictionary
approch = 1

class Answers:
    def __init__(self, ze_ic, ze_key, plain_text, E, A, T):
        self.ic = ze_ic
        self.key = ze_key
        self.plain_text = plain_text
        self.E = E
        self.A = A
        self.T = T




f = open('sowpods.txt', 'r').readlines()
common_words = open('commonwords.txt', 'r').readlines()
cipher_text = 'WJHZR DIAKZ TMCYS OMLVY HISNF BNZRP' \
              'OESFJ RVLWL MIPOA LJAKD SQWLH KYSCN' \
              'RMHPB OQNQQ MNBXC CACJN BOVVT LAUWJ' \
              'RNISI FFBJO WZWIV NCWQM AUEEX TNOMR' \
              'JIIYH ISNWD Y'



test_cipher_text = 'ALTDW ZENJD OIC' # This is a cypher
# test_cipher_text = '''
# hrjdui hpagsxuk ewl wedjo xpyopi oed hliy iomd p wsdi omeh aatiaic rvrepprtcn sws uihh hro xuzphasch yilra ed xm me
#  llvp cla l lvvvxuk apwic qf vphlecroich hx zmmscsb rtklvdxacdjnkphawewltstusxtusyxztctcewtuxngleexuklhvycrlsqtegphzz
#  zahxtapxjuvvtccidivvdxajzjuhpkphpcjiewhxewlyyblhtpaiousszsvjytdwlcksaxumzcalliwsfgzsgtyxstzsnxhpxtkmliyeyhvqctzywizm
#  yhvqphasnzzkpiamyvdltewiopysfckjzgdipzzfjioidptiqpjxdioidihppcladtmjpramdpcicnnszslblbwppdmqlgriehuseeysntzwtcnmyuvvx
#  pamzcdmewwiculgetmjtrpiyrfnfwhrtaprypprxphptzlqlcfenpkixxjwejkmphpredlufxamphalpdejzgksytlblbprpsalpdymphjewaprrxuxzf
#  bidipsyioixpyopizemxsmenasagvgphzmyuvvxpamzcdmewwiculgetmjtrpiyrfmyiomdrhwphvqpiomyvjewalhewlwepsiytdwsnwsewlwthpxdpf
#  wewhxtccidivvdeysmpipjpyiyialppbxzbhxzczsqghxtduewxacotwmnilhtcjplhzmnpsqlgriebvhpazastuxstfglcaigtuvprvkyxzihwlrlhasc
#  noedqliygltzgaiopsvppkcgdseexsmenjptbiwlewvprpemafastuedivgvxzqpcamzclhxdyizuaiyduxhxaxpgcswpamwxacnapqmhhtaglgtpipjlo
#  iypzxzrrmdblrexvrpstsctvjetusyidmeilvawvxz'''


# cipher_text = test_cipher_text
debug_flag = 0
cipher_text = cipher_text.replace(" ", '')
cipher_text = cipher_text.replace("\n", '')
cipher_text = cipher_text.replace(".", '')
cipher_text = cipher_text.replace(",", '')
cipher_text = cipher_text.replace("'", '')
cipher_text = cipher_text.replace('"', '')
cipher_text = cipher_text.replace('?', '')

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z']
count = 0
possible_answers = []

def analyse(deciphered_message, key):
    word_count = 0
    word_list = []
    words_len = 0

    # Check IC
    checkIC = co_incidence_index.CheckIC(deciphered_message)
    ic = checkIC.ic
    E = checkIC.E
    A = checkIC.A
    T = checkIC.T
    X = checkIC.X
    J = checkIC.J
    Z = checkIC.Z

#    print(ic)
#    if 'FJORD' in deciphered_message:   
#        print(ic)
#        ic = 1
    # Check ratio of words in answer
    if ic > 0.6:
        for each_key in all_keys:
            # print(each_key)

            if len(each_key) == 2:
                # pass
                continue
            if len(each_key) == 3:
                # pass
                continue
            else:
                if each_key in deciphered_message:
                    word_list.append(each_key)

        # for each_key in common_words:
        #     each_key = each_key.strip('\n').upper()
        #     if len(each_key) == 2:
        #         # pass
        #         continue
        #     if len(each_key) == 3:
        #         word_list.append(each_key)
        #         continue
        #     else:
        #         if each_key in deciphered_message:
        #             word_count += 1
        #             words_len += len(each_key)
        #             word_list.append(each_key)
        #             # lock.acquire()
        #             # print(each_key)
        #             # print(deciphered_message)
        #             # lock.release()
        words = ''.join(word_list)
        words_len = (len(words)/len(deciphered_message))
        if words_len > 0.9:
            print(words_len, len(cipher_text))
            lock.acquire()
            print('+'*20)
            print(word_list)
            print(deciphered_message)
            print(E, A, T)
            print(Z, J, X)
            # possible_answers.append(Answers(ic, each_line, deciphered_message, E, A, T))
            print(key)
            print(ic)
            lock.release()
            # exit()


def run(key):

    # print(each_line)
    # print('[threads active] %s ' % threading.active_count())


    key = [x for x in key]
    key_size = len(key)


    cipher_list_sized = [cipher_text[i:i+key_size] for i in range(0, len(cipher_text), key_size)]

    deciphered_message = ''
    for each_part in cipher_list_sized:
        x = 0
        for each_char in key:
            
            try:
                if each_char == '\n':
                    continue

                key_letter = alphabet.index(each_char.upper())
                cypher_letter = alphabet.index(each_part[x].upper())

                deciphered_letter_index = cypher_letter - key_letter

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
#    print(deciphered_message)
    analyse(deciphered_message, key)



def new_create_brute(key_size):
    arrangments = itertools.combinations_with_replacement(alphabet, key_size)
    # for each in arrangments:
    #     print(each)
    return arrangments

def create_brute():
    brute = []
    brute.append('HELP')
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
    # for each in range(0, 26, 1):
    #     print(alphabet[each] + str(5))
    #     for each1 in range(0, 26, 1):
    #         for each2 in range(0, 26, 1):
    #             for each3 in range(0, 26, 1):
    #                 for each4 in range(0, 26, 1):
    #                     brute.append(alphabet[each] + alphabet[each1] + alphabet[each2] + alphabet[each3] + alphabet[each4])

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




    # brute = create_brute()
    # brute = ['HELP']
    all_keys = [x.upper().replace('\n', '').replace(' ', '') for x in f]
    possible_sizes = kasiski.Kasiski(cipher_text).multiples_list
    possible_sizes.sort()
    print(possible_sizes)

    if approch == 0:
        keys_to_try = [new_create_brute(x) for x in possible_sizes]
        for each_key_size in possible_sizes:
            print('Brute Forcing %s' % str(each_key_size))
            key_set = new_create_brute(each_key_size)
            m = multiprocessing.Manager()
            ze_pool = multiprocessing.Pool(5)
            ze_pool.imap(worker, key_set)
            ze_pool.close()
            ze_pool.join()

    elif approch == 1:
        keys_to_try = []
        for key in all_keys:
            if len(key) in possible_sizes:
                keys_to_try.append(key)
        m = multiprocessing.Manager()
        ze_pool = multiprocessing.Pool(4)
        ze_pool.imap(worker, keys_to_try)
        ze_pool.close()
        ze_pool.join()
    else:
        keys_to_try = []
        exit()





#
#
#
#
