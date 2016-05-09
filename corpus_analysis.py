import itertools

import time



class Analyse:
    def __init__(self, ze_text):



        self.alphabet = [x for x in 'abcdefghijklmnopqrstuvwxyz']

        ze_text = ze_text.replace('\n', ' ')
        ze_text = ze_text.lower()
        self.ze_text = ''.join([x for x in ze_text if x in self.alphabet or x in ' '])
        self.words = ze_text.split(' ')
        self.result = 0
        # flat list of possible bigrams

                # print('[Name]\t\t %s ' % each.name)
                # print('[Frequncy]\t %s' % str(each.frequency))
                # print('[Known Frequency] %s' % str(each.known_frequency))

                # print(len(f))
    def run(self):
        # Create a list of all possible english bigrams
        all_possible_bigrams = itertools.product(self.alphabet, self.alphabet)
        all_possible_bigrams = list(all_possible_bigrams)
        all_possible_bigrams = [x+y for x, y in all_possible_bigrams]

        bigrams = [] # list of bigram class

        # Create a class for each possible bigram
        for each_bigram in all_possible_bigrams:
            bigrams.append(self.Bigram(each_bigram))

        # Break up the text into words, it is not required for the text to be in words though
        for each_word in self.words:
            # print(each_word)
            i = 0

            # If there are still spaces get rid of them
            each_word = each_word.replace(' ', '')

            # Until there are no characters left in the word we are looking at
            while i < len(each_word)-1:

                ze_bigram = each_word[i] + each_word[i+1]
                if len(ze_bigram) == 1:
                    break

                for each_bigram in bigrams:
                    if each_bigram.name == ze_bigram:
                        each_bigram.frequency += 1
                        i += 1
                        break

        bigrams.sort(key=lambda x: x.frequency, reverse=True)
        for each in bigrams:
            if each.frequency > 0:
                each.frequency = each.frequency/len(self.ze_text)
                if each.known_frequency+0.1 > each.frequency > each.known_frequency-0.1:
                    self.result += 1



    class Bigram:
        def __init__(self, bigram):
            self.frequent_bigrams = {
                    'TH': 1.52,
                    'EN': 0.55,
                    'NG': 0.18,
                    'HE': 1.28,
                    'ED': 0.53,
                    'OF': 0.16,
                    'IN': 0.94,
                    'TO': 0.52,
                    'AL': 0.09,
                    'ER': 0.94,
                    'IT': 0.50,
                    'DE': 0.09,
                    'AN': 0.82,
                    'OU': 0.50,
                    'SE': 0.08,
                    'RE': 0.68,
                    'EA': 0.47,
                    'LE': 0.08,
                    'ND': 0.63,
                    'HI': 0.46,
                    'SA': 0.06,
                    'AT': 0.59,
                    'IS': 0.46,
                    'SI': 0.05,
                    'ON': 0.57,
                    'OR': 0.43,
                    'AR': 0.04,
                    'NT': 0.56,
                    'TI': 0.34,
                    'VA': 0.04,
                    'HA': 0.56,
                    'AS': 0.33,
                    'RA': 0.04,
                    'ES': 0.56,
                    'TE': 0.27,
                    'LD': 0.02,
                    'ST': 0.55,
                    'ET': 0.19,
                    'UR': 0.02}
            self.name = bigram
            self.first_letter = bigram[0]
            self.second_letter = bigram[1]
            self.known_frequency = 0
            for key, value in self.frequent_bigrams.items():
                if self.name.upper() == key:

                    self.known_frequency = value/100
            self.frequency = 0







