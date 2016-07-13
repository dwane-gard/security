import itertools
from functools import reduce

class Decode:
    def __init__(self, cipher_text):
        self.cipher_text = cipher_text
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']

    def runner(self, key):
        '''
        Vigenere decryption module
        :param key:
        :return:
        '''

        # Reverse the the key
        key = key[::-1]

        pairs = zip(self.cipher_text, itertools.cycle(key))
        result = ''
        for pair in pairs:
            total = reduce(lambda x, y: self.alphabet.index(x) - self.alphabet.index(y), pair)
            result += self.alphabet[total % 26]
        return result, key

    def auto_key(self, key):
        '''
        Auto Key decryption module
        :param key:
        :return:
        '''

        # Reverse the the key
        key = key[::-1]

        message = ''
        next_key = key
        key_pos = 0
        key_length = len(key)
        while len(self.cipher_text) > key_pos:
            this_result = ''
            pairs = zip(self.cipher_text[key_pos:key_pos + key_length], itertools.cycle(next_key))
            for pair in pairs:

                total = reduce(lambda x, y: self.alphabet.index(x) - self.alphabet.index(y), pair)
                this_result += self.alphabet[total % 26]

            key_pos += key_length
            message += this_result
            next_key = this_result

        return message, key

    def beaufort_decrypt(self, key):
        '''
        Beaufort decryption module
        :param key:
        :return:
        '''

        # Reverse the the key
        key = key[::-1]

        pairs = zip(self.cipher_text, itertools.cycle(key))
        result = ''
        for pair in pairs:
            total = reduce(lambda x, y: self.alphabet.index(y) - self.alphabet.index(x), pair)
            result += self.alphabet[total % 26]
        if self.analyse_code is True:
            self.analyse(result, key)

        return result, key