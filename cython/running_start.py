# Decodes a running cipher
from packages.pad import Decode
from packages.analyse import CheckIC, ChiSquare
import itertools
import multiprocessing
import time

class Running:
    def __init__(self, cipher_text, degree):
        self.check_cipher_text = cipher_text[:degree]
        alpha = [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        self.keys = itertools.product(alpha, repeat=degree)
        self.decode = Decode(self.check_cipher_text)

    def start(self):
        ''' MultiCore '''
        q = multiprocessing.Queue(maxsize=50)
        jobs = []

        # Create workers
        for i in range(0, multiprocessing.cpu_count(), 1):
            p = multiprocessing.Process(target=self.worker, args=(q,))
            p.start()
            jobs.append(p)

        # Feed items into the queue
        for each_item in self.keys:
            q.put(each_item)

    def worker(self, q):
        while True:
            if q.empty():
                time.sleep(1)
            try:
                obj = q.get(timeout=1)
                chiSquareKey = ChiSquare(''.join(obj))
                print(''.join(obj))

                if chiSquareKey.chi_result < 150:
                    print(chiSquareKey.chi_result)
                    plain_text, key = self.decode.runner(obj)
                    chiSquarePlainText = ChiSquare(plain_text)
                    print(chiSquarePlainText.chi_result)
                    if chiSquarePlainText.chi_result < 150:
                        with open('running_cipher.txt', 'a') as results_file:
                            results_file.write('%s | %s' % (str(key), str(plain_text)))
            except:
                break
        return

if __name__ == '__main__':
    cipher_text = open('cipher_3_text.txt', 'r').read()
    cipher_text = ''.join([x for x in cipher_text if x.isalpha()])
    running = Running(cipher_text, 20)
    running.start()