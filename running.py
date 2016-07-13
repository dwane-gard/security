import itertools
import multiprocessing
import time

from brute_force_vigenere import decode
from word_search import WordSearch


class Run:
    def __init__(self, check_len, cipher_text):
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z']
        self.words = open('sowpods.txt', 'r').readlines()
        self.cipher_text = cipher_text[0:check_len+1]
        self.brute = itertools.product(self.alphabet, repeat=check_len)
        self.decoder = decode(self.cipher_text, 0)
    def start(self):
        ''' '''
        ''' MultiCore '''
        q = multiprocessing.Queue(maxsize=50)
        jobs = []


        # Create workers
        for i in range(0, multiprocessing.cpu_count(), 1):
            p = multiprocessing.Process(target=self.worker, args=(q,))
            p.start()
            jobs.append(p)

        # Feed items into the queue
        for each_item in self.brute:
            q.put(each_item)

        # Wait for each worker to finish before continueing
        for each_job in jobs:
            each_job.join()

        ''' Single Core '''
        # for each_key in self.brute:
        #     plain_text = self.decoder.run(each_key)
        #     wordSearch = WordSearch(plain_text)
        #     words_len = wordSearch.run()
        #     if words_len < 1:
        #         with open('running_results', 'a') as results_file:
        #             results_file.write('%s | %s | %s' % (str(each_key), str(plain_text), str(words_len)))
    def worker(self, q):
        while True:
            if q.empty():
                time.sleep(1)
            try:
                obj = q.get(timeout=1)
                plain_text = self.decoder.decrypt(obj)
                wordSearch = WordSearch(plain_text)
                words_len = wordSearch.run()
                print('%s | %s' % (str(obj), str(words_len)))

                if words_len > 1:
                    print(words_len)
                    print(plain_text)
                    with open('running_results.txt', 'a') as results_file:
                        results_file.write('%s | %s | %s' % (str(obj), str(plain_text), str(words_len)))
            except:
                print('[!] run finished')
                break
        print('ending worker')
        return

if __name__ == '__main__':
    cipher_text = open('cipher_3_text.txt', 'r').read()
    # cipher_text = 'THISISAVERYDERPYTHING'
    cipher_text = ''.join([x for x in cipher_text if x.isalpha()])
    run = Run(17, cipher_text)
    run.start()
