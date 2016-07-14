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

    def columnar(self, key):
        ''' Columnar Tranpositional decryption module '''

        plain_text = ''
        key_len = len(key)

        cipher_blocks = []

        return plain_text, key

    def permutation(self, key):
        ''' Permutaion Transpositional decyption module '''
        # key = key[::-1]
        key_len = len(key)
        plain_text = ''

        # pairs = zip(self.cipher_text, itertools.cycle(key))
        # for pair in pairs:
        #     total = reduce(lambda x, y: plain_text[y] = x, pair)

        cipher_blocks = [self.cipher_text[i:i+key_len] for i in range(0, len(self.cipher_text), key_len)]
        for each_block in cipher_blocks:
            for each in key:
                    # unencrypt that character and add it to the plain text
                    try:
                        plain_text += each_block[each-1]
                    except:
                        plain_text += ''
        return plain_text, key

    def one_time_pad(self, key):
        ''' One Time pad decryption module '''

        # break up cipher text into its multiple parts
        # decode each part with the given key
        # return for checking

if __name__ == '__main__':
    test_cipher = "ARESA SXOST HEYLO IIAIE XPENG DLLTA HTFAX TENHM WX"
    test_cipher = [x for x in test_cipher if x.isalpha()]
    decode = Decode(test_cipher)
    print(decode.columnar([4,2,5,1,6,3]))
