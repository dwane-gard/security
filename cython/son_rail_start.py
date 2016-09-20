from packages.analyse import Dia, CheckIC, ChiSquare, NthMessage
from packages.pre_analysis import Kasiski
from termcolor import colored
import itertools
import multiprocessing
import time

class RailFence:
    def __init__(self, cipher_text, *args):
        # cipher_text = ''.join([x for x in cipher_text if x.isalpha()])
        self.cipher_text = cipher_text
        self.known_text = args

    def digram_analysis(self):
        return

    def analyse(self):
        print(self.cipher_text.count('C'))
        print(self.cipher_text.count('O'))
        cipher_text_list = [x for x in self.cipher_text]

        for index, object in enumerate(cipher_text_list):
            if object == 'P':
                print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            #
            # elif object == 'O':
            #     print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            # elif object == 'M':
            #     print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            # elif object == 'P':
            #     print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            # elif object == '3':
            #     print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            # elif object == '4':
            #     print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            # elif object == '1':
            #     print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            # elif object == '{':
            #     print(colored('%s: %s' % (str(index+1), str(object)), 'green'))
            # elif object == ' ':
            #     print(colored('%s: %s' % (str(index+1), str(object)), 'blue'))
            # elif object == 'u':
            #         print(colored('%s: %s' % (str(index+1), str(object)), 'yellow'))
            else:
                print('%s: %s' %(str(index+1), str(object)))


            # #mp
            # first 174
            #
            # for each in [19,120,154,267,278]:
            #
            #     # find the difrence between each
            #
            #     #-101
                #-135

    def pre_analyse(self):
        checkIC = CheckIC()
        cipher_text = ''.join([x for x in self.cipher_text if x.isalpha()])
        print(cipher_text)
        print(self.cipher_text)
        print(checkIC.run(''.join([x for x in self.cipher_text if x.isalpha()])))
        # kasiski = Kasiski
        #
        # for degree in range(1,25):
        #     nthMessage = NthMessage(cipher_text, degree)
        #     print(nthMessage.output())

    def pattern_build(self):
        '''
        very dirty code to build out a custom rail fence-like cipher from a known starting point with a known pattern of
        difrence between characters
        '''

        known_set = [271,272,273,274,275,276,277,278,279,280]

        first_move = 20
        paterns = []
        for each_set in known_set:
            this_pattern = [each_set,]
            print(first_move)

            # build left
            this_pattern.insert(0, this_pattern[0] - first_move)
            first_move -= 1
            print(first_move)
            for i in range(2):
                this_pattern.insert(0, this_pattern[0] - 20)
            for i in range(4):
                this_pattern.insert(0, this_pattern[0] - 19)
            for i in range(7):
                this_pattern.insert(0, this_pattern[0] - 18)

            # build right
            this_pattern.append(this_pattern[-1] - first_move)

            for i in range(2):
                this_pattern.append(this_pattern[-1] - 20)
            for i in range(4):
                this_pattern.append(this_pattern[-1] - 19)
            for i in range(7):
                this_pattern.append(this_pattern[-1] - 18)

            # this_pattern = [x-1 for x in this_pattern]

            paterns.append(this_pattern)
            print(this_pattern)

        # build out the plain text from index in cipher text
        for patern in paterns:
            self.cipher_text = [x for x in self.cipher_text]
            plain_text = [self.cipher_text[x-1] for x in patern]

            print(''.join(plain_text))

        for each in range(1,280,1):
            if each not in [item for sublist in paterns for item in sublist]:
                print(each)

class Redefence:
    ''' Class is for breaking redefence (railfence with a key from a brute force perspective'''
    def __init__(self, key, cipher_text, degree):
        cipher_text = "S_   ltes e__owesft4ya'h r_ernadinhohn_hstfeamion coo iost  lhrooidskeutsio t,aPeeut_eemlc tmkhegi_wschoool31neOen Cbale4h s tee_  oi_r yjnsr  iat_.>dslu}4 nd asthsnCg\  it_ Misdirection_tCaeesa Oe1elr__firiOR_lelsmk_hlabsfkabM{fbbliuec_p  eiecn P1oaubco a_ite_headm34rebihchtHo4c"
        degree = 15
        # key = key + (11,12,13,14) 1


        self.cipher_text = [x for x in cipher_text]
        standard_list_len = int(len(cipher_text) / (degree-1))
        cipher_lists = [[] for x in range(degree)]

        # Build out the 'columns' of the cipher text which will be moved around depending on the key
        for each_key_char in key:
            if each_key_char == min(key) or each_key_char == max(key):
                count = int(standard_list_len/2)
            else:
                count = standard_list_len

            while count > 0:
                cipher_char = self.cipher_text[0]
                del self.cipher_text[0]
                cipher_lists[each_key_char].append(cipher_char)
                count -= 1

        plain_text = ''
        decending = True
        i = 0

        # get the plain text from cipher text indexes
        while True:
            if len(plain_text) == len(cipher_text):
                break

            plain_char = cipher_lists[i][0]
            plain_text += plain_char
            del cipher_lists[i][0]

            if i == 0:
                decending = True
            elif i == degree -1:
                decending = False

            if decending is True:
                i += 1
            else:
                i -= 1

        # check for known text
        if 'OMP3441{' in plain_text:
            with open('redefence.txt', 'a') as results_file:
                results_file.write('%s : %s\n' % (str(key), plain_text))
        print(plain_text)
        time.sleep(10)


class MorphingRailFence:
    '''
    For brute forcing a rail fence cipher that has a morphing patern, this is UNFINISHED
    '''
    def __init__(self, key):
        cipher_text = "S_   ltes e__owesft4ya'h r_ernadinhohn_hstfeamion coo iost  lhrooidskeutsio t,aPeeut_eemlc tmkhegi_wschoool31neOen Cbale4h s tee_  oi_r yjnsr  iat_.>dslu}4 nd asthsnCg\  it_ Misdirection_tCaeesa Oe1elr__firiOR_lelsmk_hlabsfkabM{fbbliuec_p  eiecn P1oaubco a_ite_headm34rebihchtHo4c"
        degree = 15
        # key = key + (11,12,13,14)
        print(key)

        self.cipher_text = [x for x in cipher_text]

        standard_list_len = int(len(cipher_text) / (degree - 1))
        cipher_lists = [[] for x in range(degree)]

        # print(standard_list_len)

        for each_key_char in key:
            # print('key char: %d' % each_key_char)
            if each_key_char == min(key) or each_key_char == max(key):
                count = int(standard_list_len / 2)
            else:
                count = standard_list_len

            while count > 0:
                # print(count)
                # print('Cipher text pos: %d' % len(self.cipher_text))

                cipher_char = self.cipher_text[0]
                # print(cipher_char)
                del self.cipher_text[0]
                cipher_lists[each_key_char].append(cipher_char)
                count -= 1

        for each in cipher_lists:
            print(''.join(each))
        # exit()

        plain_text = ''
        decending = True
        i = 0
        while True:

            if len(plain_text) == len(cipher_text):
                break

            plain_char = cipher_lists[i][0]

            plain_text += plain_char
            # print(plain_text)
            del cipher_lists[i][0]

            if i == 0:
                decending = True
            elif i == 14:
                decending = False

            if decending is True:
                i += 1
            else:
                i -= 1

        if 'OMP3441{' in plain_text:
            with open('redefence.txt', 'a') as results_file:
                results_file.write('%s : %s\n' % (str(key), plain_text))
        print(plain_text)
        time.sleep(10)


def worker(q):
    while True:
        if q.empty():
            time.sleep(1)

        try:
            obj = q.get(timeout=1)
            Redefence(obj)

        except:
            # print('[!] run finished')
            break
    # print('ending worker')
    return

def npermuatations(amount_of_numbers, length_of_set):
    ''' Discover the number of permutations'''
    n = range(1, amount_of_numbers+1 , 1)
    r = range(1, (amount_of_numbers+1 - length_of_set+1), 1)

    running_answer = 1
    for each in n:
        running_answer = each * running_answer
    n = running_answer

    running_answer = 1
    for each in r:
        running_answer = each * running_answer
    r = running_answer

    return int(n/r)

if __name__ == '__main__':

    ''' Analyse '''
    railFence = RailFence('''S_   ltes e__owesft4ya'h r_ernadinhohn_hstfeamion coo iost  lhrooidskeutsio t,aPeeut_eemlc tmkhegi_wschoool31neOen Cbale4h s tee_  oi_r yjnsr  iat_.>dslu}4 nd asthsnCg\  it_ Misdirection_tCaeesa Oe1elr__firiOR_lelsmk_hlabsfkabM{fbbliuec_p  eiecn P1oaubco a_ite_headm34rebihchtHo4c'''
                          , 'COMP3441{')
    railFence.pre_analyse()
    railFence.analyse()
    railFence.pattern_build()

    ''' Single Thread '''
    # keys = itertools.permutations(range(0, 11, 1))
    # keys = [(14,13,12,11,10,9,8,7,6,5,4,3,2,1,0),]
    # keys = [(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14)]
    # for each_key in keys:
    #     Redefence(each_key)
    ''' Multi Thread '''
    # keys = itertools.permutations(range(0, 10, 1))
    # number_of_permutations = npermuatations(10, 10)
    #
    # count = 0
    #
    # for each in range(0, number_of_permutations, 100000):
    #     current_keys = itertools.islice(keys, count, each)
    #     count = each
    #
    #     # Pool
    #     chunksize = (20 * multiprocessing.cpu_count())
    #     p = multiprocessing.Pool(multiprocessing.cpu_count())
    #     p.map_async(Redefence, current_keys, chunksize=chunksize)
    #     p.close()
    #     p.join()




# known plain texts
# lbubble
# licious
#  me hack
# ___ciph
# l the a
# be_this
# feeHack
# t's the d _random_bit done, the
#  flag is COMP3441{Rail_CiPher
# forceab
