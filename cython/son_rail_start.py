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
            if object == 'C':
                print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            elif object == 'O':
                print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            elif object == 'M':
                print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            elif object == 'P':
                print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            elif object == '3':
                print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            elif object == '4':
                print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            elif object == '1':
                print(colored('%s: %s' % (str(index+1), str(object)), 'red'))
            elif object == '{':
                print(colored('%s: %s' % (str(index+1), str(object)), 'green'))
            elif object == ' ':
                print(colored('%s: %s' % (str(index+1), str(object)), 'blue'))
            elif object == 'u':
                    print(colored('%s: %s' % (str(index+1), str(object)), 'yellow'))
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

class Redefence:
    def __init__(self, key):
        cipher_text = "S_   ltes e__owesft4ya'h r_ernadinhohn_hstfeamion coo iost  lhrooidskeutsio t,aPeeut_eemlc tmkhegi_wschoool31neOen Cbale4h s tee_  oi_r yjnsr  iat_.>dslu}4 nd asthsnCg\  it_ Misdirection_tCaeesa Oe1elr__firiOR_lelsmk_hlabsfkabM{fbbliuec_p  eiecn P1oaubco a_ite_headm34rebihchtHo4c"
        degree = 15
        key = key + (11,12,13,14)
        print(key)
        self.cipher_text = [x for x in cipher_text]

        standard_list_len = int(len(cipher_text) / (degree-1))
        cipher_lists = [[] for x in range(degree)]
        # print(cipher_lists)
        # print(standard_list_len)

        for each_key_char in key:
            # print('key char: %d' % each_key_char)
            if each_key_char == min(key) or each_key_char == max(key):
                count = int(standard_list_len/2)
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

        # for each in cipher_lists:
        #     print(each)
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

        if 'COMP3441{' in plain_text:
            with open('redefence.txt', 'a') as results_file:
                results_file.write('%s : %s' % (str(key), plain_text))
            print(plain_text)






class MorphingRailFence:
    def __init__(self, cipher_text, key_size):
        self.cipher_text = cipher_text
        self.structure = [[None] * len(cipher_text) for n in range(key_size)]
        self.plain_text = ''
    # def run(self):


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

if __name__ == '__main__':

    # railFence = RailFence('''
    # S_   ltes e__owesft4ya'h r_ernadinhohn_hstfeamion coo iost  lhrooidskeutsio t,aPeeut_eemlc tmkhegi_wschoool31neOen Cbale4h s tee_  oi_r yjnsr  iat_.>dslu}4 nd asthsnCg\  it_ Misdirection_tCaeesa Oe1elr__firiOR_lelsmk_hlabsfkabM{fbbliuec_p  eiecn P1oaubco a_ite_headm34rebihchtHo4c
    # '''
    #                       , 'COMP3441{')
    # railFence.pre_analyse()
    # railFence.analyse()
    #

    keys = itertools.permutations(range(0,11,1))

    # Process
    q = multiprocessing.Queue(maxsize=50)
    jobs = []

    # Create workers
    for i in range(0, multiprocessing.cpu_count()-1, 1):
        p = multiprocessing.Process(target=worker, args=(q,))
        p.start()
        jobs.append(p)

    # Feed items into the queue
    for each_item in keys:
        q.put(each_item)

    # Wait for each worker to finish before continueing
    for each_job in jobs:
        each_job.join()

    # Pool
    # p = multiprocessing.Pool(multiprocessing.cpu_count())
    # p.imap(Redefence, keys)
    # p.close()
    # p.join()

# known plain texts
# lbubble
# licious
#  me hack
# ___ciph
# l the a
# be_this
# feeHack
# MP3441{
# forceab
