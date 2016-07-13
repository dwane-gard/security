class WordSearch:
    def __init__(self):
        self.keys = open('sowpods.txt', 'r').readlines()
        self.keys = [x[0:-1].upper() for x in self.keys]
        self.keys = [x for x in self.keys if len(x) != 2]
        self.keys = [x for x in self.keys if len(x) != 3]
        self.len_plain_text = None

    def run(self, plain_text):
        word_list = []
        for each_key in self.keys:
            if each_key in plain_text:
                word_list.append(each_key)
        if self.len_plain_text is None:
            self.len_plain_text = len(plain_text)
        words_list_len = len(''.join(word_list))
        words_len = words_list_len/self.len_plain_text
        return words_len

    def the_check(self, plain_text):
        the_count = plain_text.count('THE')
        return the_count

class CheckIC:
    def __init__(self):
        alphabet = [x for x in'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        self.text_size = None
        self.text_changes = True
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.F = 0
        self.G = 0
        self.H = 0
        self.I = 0
        self.J = 0
        self.K = 0
        self.L = 0
        self.M = 0
        self.N = 0
        self.O = 0
        self.P = 0
        self.Q = 0
        self.R = 0
        self.S = 0
        self.T = 0
        self.U = 0
        self.V = 0
        self.W = 0
        self.X = 0
        self.Y = 0
        self.Z = 0

        self.ic = 0
    def run(self, plain_text):

        # Check if we need to do text changes on first operation, using as a case study for the rest
        if self.text_changes is True:
            original_plain_text = plain_text
            plain_text = ''.join([x for x in plain_text if x.isalpha()])
            plain_text = ''.join([x.upper() for x in plain_text])
            if original_plain_text == plain_text:
                self.text_changes = True
            else:
                self.text_changes = False

        if self.text_size is None:
            self.text_size = len(plain_text)

        self.A = plain_text.count('A')
        self.B = plain_text.count('B')
        self.C = plain_text.count('C')
        self.D = plain_text.count('D')
        self.E = plain_text.count('E')
        self.F = plain_text.count('F')
        self.G = plain_text.count('G')
        self.H = plain_text.count('H')
        self.I = plain_text.count('I')
        self.J = plain_text.count('J')
        self.K = plain_text.count('K')
        self.L = plain_text.count('L')
        self.M = plain_text.count('M')
        self.N = plain_text.count('N')
        self.O = plain_text.count('O')
        self.P = plain_text.count('P')
        self.Q = plain_text.count('Q')
        self.R = plain_text.count('R')
        self.S = plain_text.count('S')
        self.T = plain_text.count('T')
        self.U = plain_text.count('U')
        self.V = plain_text.count('V')
        self.W = plain_text.count('W')
        self.X = plain_text.count('X')
        self.Y = plain_text.count('Y')
        self.Z = plain_text.count('Z')

        letters = [self.A, self.B, self.C, self.D, self.E, self.F, self.G, self.H, self.I, self.J, self.K, self.L, self.M, self.N, self.O, self.P, self.Q, self.R, self.S, self.T, self.U, self.V, self.W, self.X, self.Y, self.Z]

        freqsum = 0
        for each_letter in letters:
            freqsum += each_letter * (each_letter - 1)

        self.ic = freqsum / (self.text_size * (self.text_size - 1))

        return float(self.ic)


class ChiSquare:
    def __init__(self, plain_text):
        alphabet = [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']

        self.plain_text = ''.join([x.upper() for x in plain_text if x.isalpha()])
        checkIC = CheckIC()
        checkIC.run(self.plain_text)
        self.ic = checkIC.ic
        self.chi = [self.CheckLetter(getattr(checkIC, x), len(self.plain_text), x) for x in alphabet]
        self.chi_result = sum([x.result for x in self.chi])

    def output(self):
        return self.chi_result

    class CheckLetter:
        def __init__(self, letter_count, text_count, letter):
            self.letter_count = letter_count
            self.text_count = text_count
            self.letter = letter

            self.expected_frequency = 0
            self.find_expected_frequency()

            self.result = self.run()

        def run(self):

            expected_count = self.text_count*self.expected_frequency
            result = ((self.letter_count - expected_count)**2) / expected_count
            return result

        def find_expected_frequency(self):
            if self.letter == 'E':
                self.expected_frequency = 0.127
            elif self.letter == 'A':
                self.expected_frequency = 0.082
            elif self.letter == 'B':
                self.expected_frequency = 0.015
            elif self.letter == 'C':
                self.expected_frequency = 0.028
            elif self.letter == 'D':
                self.expected_frequency = 0.043
            elif self.letter == 'F':
                self.expected_frequency = 0.022
            elif self.letter == 'G':
                self.expected_frequency = 0.02
            elif self.letter == 'H':
                self.expected_frequency = 0.061
            elif self.letter == 'I':
                self.expected_frequency = 0.07
            elif self.letter == 'J':
                self.expected_frequency = 0.002
            elif self.letter == 'K':
                self.expected_frequency = 0.008
            elif self.letter == 'L':
                self.expected_frequency = 0.04
            elif self.letter == 'M':
                self.expected_frequency = 0.024
            elif self.letter == 'N':
                self.expected_frequency = 0.067
            elif self.letter == 'O':
                self.expected_frequency = 0.075
            elif self.letter == 'P':
                self.expected_frequency = 0.019
            elif self.letter == 'Q':
                self.expected_frequency = 0.001
            elif self.letter == 'R':
                self.expected_frequency = 0.06
            elif self.letter == 'S':
                self.expected_frequency = 0.063
            elif self.letter == 'T':
                self.expected_frequency = 0.091
            elif self.letter == 'U':
                self.expected_frequency = 0.028
            elif self.letter == 'V':
                self.expected_frequency = 0.01
            elif self.letter == 'W':
                self.expected_frequency = 0.024
            elif self.letter == 'X':
                self.expected_frequency = 0.002
            elif self.letter == 'Y':
                self.expected_frequency = 0.02
            elif self.letter == 'Z':
                self.expected_frequency = 0.001

