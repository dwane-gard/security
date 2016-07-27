import itertools
from functools import reduce
import time
from pad import Decode

class NthMessage:
    ''' breaks up the cipher text of  vigenere cipher into its parts so it can be treaded as a ceaser shift cipher'''
    def __init__(self, cipher_text, degree):

        self.cipher_text = cipher_text
        self.cipher_columns = []
        self.plain_texts = []

        j = 0
        while j < degree:
            i = j
            nth_cypher_text = ''
            while i < len(self.cipher_text):
                nth_cypher_text += self.cipher_text[i]
                i += degree
            j += 1
            # print(nth_cypher_text)
            self.cipher_columns.append(nth_cypher_text)

        for each_column in self.cipher_columns:
            Decoder = Decode(each_column)
            result = []
            # For each shift posibility decode
            for each_letter in [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']:
                result.append(self.EachMessage(each_letter, Decoder))

                # sort each part by its chi of the english language
                result.sort(key=lambda x: x.chi)

            self.plain_texts.append(result)

            # print(result[0].chi)
            # print(result[0].shift)
            # print(result[0].ic)

    def output(self):
        return self.plain_texts

    class EachMessage:
        def __init__(self, shift, Decoder):
            self.shift = shift

            # run a Vigenere decrypter
            self.plain_text, key = Decoder.runner(self.shift)

            # run a beufort decrypter
            # self.plain_text = Decoder.beaufort_decrypt(self.shift)

            self.chiSquare = ChiSquare(self.plain_text)
            self.chi = self.chiSquare.chi_result
            self.ic = self.chiSquare.ic







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
            plain_text = ''.join([x.upper() for x in plain_text if x.isalpha()])
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
        if 0.073 > self.ic:
            self.ic_difference = 0.073 - self.ic
        else:
            self.ic_difference = self.ic - 0.073
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
                self.expected_frequency = 0.1237
            elif self.letter == 'A':
                self.expected_frequency = 0.0821
            elif self.letter == 'B':
                self.expected_frequency = 0.0150
            elif self.letter == 'C':
                self.expected_frequency = 0.0230
            elif self.letter == 'D':
                self.expected_frequency = 0.0479
            elif self.letter == 'F':
                self.expected_frequency = 0.0225
            elif self.letter == 'G':
                self.expected_frequency = 0.0208
            elif self.letter == 'H':
                self.expected_frequency = 0.0645
            elif self.letter == 'I':
                self.expected_frequency = 0.0676
            elif self.letter == 'J':
                self.expected_frequency = 0.0018
            elif self.letter == 'K':
                self.expected_frequency = 0.0087
            elif self.letter == 'L':
                self.expected_frequency = 0.0393
            elif self.letter == 'M':
                self.expected_frequency = 0.0254
            elif self.letter == 'N':
                self.expected_frequency = 0.0705
            elif self.letter == 'O':
                self.expected_frequency = 0.0767
            elif self.letter == 'P':
                self.expected_frequency = 0.0163
            elif self.letter == 'Q':
                self.expected_frequency = 0.0009
            elif self.letter == 'R':
                self.expected_frequency = 0.0550
            elif self.letter == 'S':
                self.expected_frequency = 0.0617
            elif self.letter == 'T':
                self.expected_frequency = 0.0921
            elif self.letter == 'U':
                self.expected_frequency = 0.0291
            elif self.letter == 'V':
                self.expected_frequency = 0.0087
            elif self.letter == 'W':
                self.expected_frequency = 0.0254
            elif self.letter == 'X':
                self.expected_frequency = 0.0013
            elif self.letter == 'Y':
                self.expected_frequency = 0.0195
            elif self.letter == 'Z':
                self.expected_frequency = 0.0006


class Dia:
    '''
    A Pre-analysis for transposition ciphers that tries to predict the cypher by using
    diagram analysis
    '''
    def __init__(self, cipher_text, degree):
        self.cipher_text = cipher_text
        self.degree = degree
        self.cipher_columns = None
        self.data_set = []
        self.key = None

    def permutation(self):
        ''' setup the 'colmns' for a permutation cipher '''
        self.cipher_columns = [self.cipher_text[i:i + self.degree] for i in range(0, len(self.cipher_text), self.degree)]

    def columar(self):
        ''' setup the 'colmbs' for a columb cipher, not yey implementd'''
        from math import ceil
        column_len = ceil(len(cipher_text) / self.degree)
        null_count = (self.degree * column_len) - len(cipher_text)

        # we appear to need to key to know where to put the nulls, might have to have a seperate dia class to do this

    def run(self):
        # Test the probability of each diagram
        possible_diagrams = itertools.permutations(range(0, self.degree, 1), 2)
        for each in possible_diagrams:
            data = self.Data(each[0], each[1], self.cipher_columns)
            self.data_set.append(data)

        # Using the diagram probability data find the best scoring possibility for each position
        #  and build the refined data set
        refined_data_set = []
        for each_row in range(0, self.degree, 1):
            current_score = -99999999999
            top_data = None
            for each_data in self.data_set:
                if each_data.pos1 == each_row:
                    if each_data.score > current_score:
                        top_data = each_data
                        current_score = each_data.score
            if top_data.score > 0:
                refined_data_set.append(top_data)

        # packages to see if the degree has a high enough ave score to be considered
        ave_score = sum([x.score for x in refined_data_set])
        if ave_score < 1:
            # print("[!] Ave score is %f, this isn't the right degree" % ave_score)
            return
        else:
            # print("[!] Ave score is %f, this is high enough to consider" % ave_score)
            pass

        # Sort the refined data set and find the best place to start building the key
        refined_data_set.sort(key=lambda x: x.score)
        refined_data_set.reverse()

        # for each in self.data_set:
        #     print(each.pos1, each.pos2)
        #     print(each.score)

       # Build out the key
        key = [refined_data_set[0].pos1, refined_data_set[0].pos2]

        count = 0
        while True:
            for each in refined_data_set:
                if each is refined_data_set[0]:
                    pass

                if each.pos1 == key[-1]:
                    key.append(each.pos2)

                if each.pos2 == key[0]:
                    key.insert(0, each.pos1)

            if len(key) == self.degree:
                break
            count += 1
            if count == self.degree+1:
                key = None
                break

        self.key = key

    class Data:
        def __init__(self, pos1, pos2, cipher_columns):
            self.pos1 = pos1
            self.pos2 = pos2
            self.cipher_columns = cipher_columns

            self.score = self.get_average_probability(pos1, pos2)
            # print(self.score)

        class FrequencyDiagrams:
            def __init__(self):
                ''' Known Freuency of diagrams over 10000 characters of text,
                 sample is from english novels of approx. 3.2 million characters '''

                self.AA = 1
                self.AB = 20
                self.AC = 33
                self.AD = 52
                self.AE = 0
                self.AF = 12
                self.AG = 18
                self.AH = 5
                self.AI = 39
                self.AJ = 1
                self.AK = 12
                self.AL = 57
                self.AM = 26
                self.AN = 181
                self.AO = 1
                self.AP = 20
                self.AQ = 1
                self.AR = 75
                self.AS = 95
                self.AT = 104
                self.AU = 9
                self.AV = 20
                self.AW = 13
                self.AX = 1
                self.AY = 26
                self.AZ = 1

                self.BA = 11
                self.BB = 1
                self.BC = 0
                self.BD = 0
                self.BE = 47
                self.BF = 0
                self.BG = 0
                self.BH = 0
                self.BI = 6
                self.BJ = 1
                self.BK = 0
                self.BL = 17
                self.BM = 0
                self.BN = 0
                self.BO = 19
                self.BP = 0
                self.BQ = 0
                self.BR = 11
                self.BS = 2
                self.BT = 1
                self.BU = 21
                self.BV = 0
                self.BW = 0
                self.BX = 0
                self.BY = 11
                self.BZ = 0

                self.CA = 31
                self.CB = 0
                self.CC = 4
                self.CD = 0
                self.CE = 38
                self.CF = 0
                self.CG = 0
                self.CH = 38
                self.CI = 10
                self.CJ = 0
                self.CK = 18
                self.CL = 9
                self.CM = 0
                self.CN = 0
                self.CO = 45
                self.CP = 0
                self.CQ = 1
                self.CR = 11
                self.CS = 1
                self.CT = 15
                self.CU = 7
                self.CV = 0
                self.CW = 0
                self.CX = 0
                self.CY = 1
                self.CZ = 0

                self.DA = 48
                self.DB = 20
                self.DC = 9
                self.DD = 13
                self.DE = 57
                self.DF = 11
                self.DG = 7
                self.DH = 25
                self.DI = 50
                self.DJ = 3
                self.DK = 1
                self.DL = 11
                self.DM = 14
                self.DN = 16
                self.DO = 41
                self.DP = 6
                self.DQ = 0
                self.DR = 14
                self.DS = 35
                self.DT = 56
                self.DU = 10
                self.DV = 2
                self.DW = 19
                self.DX = 0
                self.DY = 10
                self.DZ = 0

                self.EA = 110
                self.EB = 23
                self.EC = 45
                self.ED = 126
                self.EE = 48
                self.EF = 30
                self.EG = 15
                self.EH = 33
                self.EI = 41
                self.EJ = 3
                self.EK = 5
                self.EL = 55
                self.EM = 47
                self.EN = 111
                self.EO = 33
                self.EP = 28
                self.EQ = 2
                self.ER = 169
                self.ES = 115
                self.ET = 83
                self.EU = 6
                self.EV = 24
                self.EW = 50
                self.EX = 9
                self.EY = 26
                self.EZ = 0

                self.FA = 25
                self.FB = 2
                self.FC = 3
                self.FD = 2
                self.FE = 20
                self.FF = 11
                self.FG = 1
                self.FH = 8
                self.FI = 23
                self.FJ = 1
                self.FK = 0
                self.FL = 8
                self.FM = 5
                self.FN = 1
                self.FO = 40
                self.FP = 2
                self.FQ = 0
                self.FR = 16
                self.FS = 5
                self.FT = 37
                self.FU = 8
                self.FV = 0
                self.FW = 3
                self.FX = 0
                self.FY = 2
                self.FZ = 0

                self.GA = 24
                self.GB = 3
                self.GC = 2
                self.GD = 2
                self.GE = 28
                self.GF = 3
                self.GG = 4
                self.GH = 35
                self.GI = 18
                self.GJ = 1
                self.GK = 0
                self.GL = 7
                self.GM = 3
                self.GN = 4
                self.GO = 23
                self.GP = 1
                self.GQ = 0
                self.GR = 12
                self.GS = 9
                self.GT = 16
                self.GU = 7
                self.GV = 0
                self.GW = 5
                self.GX = 0
                self.GY = 1
                self.GZ = 0

                self.HA = 114
                self.HB = 2
                self.HC = 2
                self.HD = 1
                self.HE = 302
                self.HF = 2
                self.HG = 1
                self.HH = 6
                self.HI = 97
                self.HJ = 0
                self.HK = 0
                self.HL = 2
                self.HM = 3
                self.HN = 1
                self.HO = 49
                self.HP = 1
                self.HQ = 0
                self.HR = 8
                self.HS = 5
                self.HT = 32
                self.HU = 8
                self.HV = 0
                self.HW = 4
                self.HX = 0
                self.HY = 4
                self.HZ = 0

                self.IA = 10
                self.IB = 5
                self.IC = 32
                self.ID = 33
                self.IE = 23
                self.IF = 17
                self.IG = 25
                self.IH = 6
                self.II = 1
                self.IJ = 1
                self.IK = 8
                self.IL = 37
                self.IM = 37
                self.IN = 179
                self.IO = 24
                self.IP = 6
                self.IQ = 0
                self.IR = 27
                self.IS = 86
                self.IT = 93
                self.IU = 1
                self.IV = 14
                self.IW = 7
                self.IX = 2
                self.IY = 0
                self.IZ = 2

                self.JA = 2
                self.JB = 0
                self.JC = 0
                self.JD = 0
                self.JE = 2
                self.JF = 0
                self.JG = 0
                self.JH = 0
                self.JI = 3
                self.JJ = 0
                self.JK = 0
                self.JL = 0
                self.JM = 0
                self.JN = 0
                self.JO = 3
                self.JP = 0
                self.JQ = 0
                self.JR = 0
                self.JS = 0
                self.JT = 0
                self.JU = 8
                self.JV = 0
                self.JW = 0
                self.JX = 0
                self.JY = 0
                self.JZ = 0

                self.KA = 6
                self.KB = 1
                self.KC = 1
                self.KD = 1
                self.KE = 29
                self.KF = 1
                self.KG = 0
                self.KH = 2
                self.KI = 14
                self.KJ = 0
                self.KK = 0
                self.KL = 2
                self.KM = 1
                self.KN = 9
                self.KO = 4
                self.KP = 0
                self.KQ = 0
                self.KR = 0
                self.KS = 5
                self.KT = 4
                self.KU = 1
                self.KV = 0
                self.KW = 2
                self.KX = 0
                self.KY = 2
                self.KZ = 0

                self.LA = 40
                self.LB = 3
                self.LC = 2
                self.LD = 36
                self.LE = 64
                self.LF = 10
                self.LG = 1
                self.LH = 4
                self.LI = 47
                self.LJ = 0
                self.LK = 3
                self.LL = 56
                self.LM = 4
                self.LN = 2
                self.LO = 41
                self.LP = 3
                self.LQ = 0
                self.LR = 2
                self.LS = 11
                self.LT = 15
                self.LU = 8
                self.LV = 3
                self.LW = 5
                self.LX = 0
                self.LY = 31
                self.LZ = 0

                self.MA = 44
                self.MB = 7
                self.MC = 1
                self.MD = 1
                self.ME = 68
                self.MF = 2
                self.MG = 1
                self.MH = 3
                self.MI = 25
                self.MJ = 0
                self.MK = 0
                self.ML = 1
                self.MM = 5
                self.MN = 2
                self.MO = 29
                self.MP = 11
                self.MQ = 0
                self.MR = 3
                self.MS = 10
                self.MT = 9
                self.MU = 8
                self.MV = 0
                self.MW = 4
                self.MX = 0
                self.MY = 18
                self.MZ = 0

                self.NA = 40
                self.NB = 7
                self.NC = 25
                self.ND = 146
                self.NE = 66
                self.NF = 8
                self.NG = 92
                self.NH = 16
                self.NI = 33
                self.NJ = 2
                self.NK = 8
                self.NL = 9
                self.NM = 7
                self.NN = 8
                self.NO = 60
                self.NP = 4
                self.NQ = 1
                self.NR = 3
                self.NS = 33
                self.NT = 106
                self.NU = 6
                self.NV = 2
                self.NW = 12
                self.NX = 0
                self.NY = 11
                self.NZ = 0

                self.OA = 16
                self.OB = 12
                self.OC = 13
                self.OD = 18
                self.OE = 5
                self.OF = 80
                self.OG = 7
                self.OH = 11
                self.OI = 12
                self.OJ = 1
                self.OK = 13
                self.OL = 26
                self.OM = 48
                self.ON = 106
                self.OO = 36
                self.OP = 15
                self.OQ = 0
                self.OR = 84
                self.OS = 28
                self.OT = 57
                self.OU = 115
                self.OV = 12
                self.OW = 46
                self.OX = 0
                self.OY = 5
                self.OZ = 1

                self.PA = 23
                self.PB = 1
                self.PC = 0
                self.PD = 0
                self.PE = 30
                self.PF = 1
                self.PG = 0
                self.PH = 3
                self.PI = 12
                self.PJ = 0
                self.PK = 0
                self.PL = 15
                self.PM = 1
                self.PN = 0
                self.PO = 21
                self.PP = 10
                self.PQ = 0
                self.PR = 18
                self.PS = 5
                self.PT = 11
                self.PU = 6
                self.PV = 0
                self.PW = 1
                self.PX = 0
                self.PY = 1
                self.PZ = 0

                self.QA = 0
                self.QB = 0
                self.QC = 0
                self.QD = 0
                self.QE = 0
                self.QF = 0
                self.QG = 0
                self.QH = 0
                self.QI = 0
                self.QJ = 0
                self.QK = 0
                self.QL = 0
                self.QM = 0
                self.QN = 0
                self.QO = 0
                self.QP = 0
                self.QQ = 0
                self.QR = 0
                self.QS = 0
                self.QT = 0
                self.QU = 9
                self.QV = 0
                self.QW = 0
                self.QX = 0
                self.QY = 0
                self.QZ = 0

                self.RA = 50
                self.RB = 7
                self.RC = 10
                self.RD = 20
                self.RE = 133
                self.RF = 8
                self.RG = 10
                self.RH = 12
                self.RI = 50
                self.RJ = 1
                self.RK = 8
                self.RL = 10
                self.RM = 14
                self.RN = 16
                self.RO = 55
                self.RP = 6
                self.RQ = 0
                self.RR = 14
                self.RS = 37
                self.RT = 42
                self.RU = 12
                self.RV = 4
                self.RW = 11
                self.RX = 0
                self.RY = 21
                self.RZ = 0

                self.SA = 67
                self.SB = 11
                self.SC = 17
                self.SD = 7
                self.SE = 74
                self.SF = 11
                self.SG = 4
                self.SH = 50
                self.SI = 49
                self.SJ = 2
                self.SK = 6
                self.SL = 13
                self.SM = 12
                self.SN = 10
                self.SO = 57
                self.SP = 20
                self.SQ = 2
                self.SR = 4
                self.SS = 43
                self.ST = 109
                self.SU = 20
                self.SV = 2
                self.SW = 24
                self.SX = 0
                self.SY = 4
                self.SZ = 0

                self.TA = 59
                self.TB = 10
                self.TC = 11
                self.TD = 7
                self.TE = 75
                self.TF = 9
                self.TG = 3
                self.TH = 330
                self.TI = 76
                self.TJ = 1
                self.TK = 2
                self.TL = 17
                self.TM = 11
                self.TN = 7
                self.TO = 115
                self.TP = 4
                self.TQ = 0
                self.TR = 28
                self.TS = 34
                self.TT = 56
                self.TU = 17
                self.TV = 1
                self.TW = 31
                self.TX = 0
                self.TY = 16
                self.TZ = 0

                self.UA = 7
                self.UB = 5
                self.UC = 12
                self.UD = 7
                self.UE = 7
                self.UF = 2
                self.UG = 14
                self.UH = 2
                self.UI = 8
                self.UJ = 0
                self.UK = 1
                self.UL = 34
                self.UM = 8
                self.UN = 36
                self.UO = 1
                self.UP = 16
                self.UQ = 0
                self.UR = 44
                self.US = 35
                self.UT = 48
                self.UU = 0
                self.UV = 0
                self.UW = 2
                self.UX = 0
                self.UY = 1
                self.UZ = 0

                self.VA = 5
                self.VB = 0
                self.VC = 0
                self.VD = 65
                self.VE = 0
                self.VF = 0
                self.VG = 0
                self.VH = 11
                self.VI = 0
                self.VJ = 0
                self.VK = 0
                self.VL = 0
                self.VM = 0
                self.VN = 0
                self.VO = 4
                self.VP = 0
                self.VQ = 0
                self.VR = 0
                self.VS = 0
                self.VT = 0
                self.VU = 0
                self.VV = 0
                self.VW = 0
                self.VX = 0
                self.VY = 1
                self.VZ = 0

                self.WA = 66
                self.WB = 1
                self.WC = 1
                self.WD = 2
                self.WE = 39
                self.WF = 1
                self.WG = 0
                self.WH = 44
                self.WI = 39
                self.WJ = 0
                self.WK = 0
                self.WL = 2
                self.WM = 1
                self.WN = 12
                self.WO = 29
                self.WP = 0
                self.WQ = 0
                self.WR = 3
                self.WS = 4
                self.WT = 4
                self.WU = 1
                self.WV = 0
                self.WW = 2
                self.WX = 0
                self.WY = 1
                self.WZ = 0

                self.XA = 1
                self.XB = 0
                self.XC = 2
                self.XD = 0
                self.XE = 1
                self.XF = 0
                self.XG = 0
                self.XH = 0
                self.XI = 2
                self.XJ = 0
                self.XK = 0
                self.XL = 0
                self.XM = 0
                self.XN = 0
                self.XO = 0
                self.XP = 3
                self.XQ = 0
                self.XR = 0
                self.XS = 0
                self.XT = 3
                self.XU = 0
                self.XV = 0
                self.XW = 0
                self.XX = 0
                self.XY = 0
                self.XZ = 0

                self.YA = 18
                self.YB = 7
                self.YC = 6
                self.YD = 6
                self.YE = 14
                self.YF = 7
                self.YG = 3
                self.YH = 10
                self.YI = 11
                self.YJ = 1
                self.YK = 1
                self.YL = 4
                self.YM = 6
                self.YN = 3
                self.YO = 36
                self.YP = 4
                self.YQ = 0
                self.YR = 3
                self.YS = 19
                self.YT = 20
                self.YU = 1
                self.YV = 1
                self.YW = 12
                self.YX = 0
                self.YY = 2
                self.YZ = 0

                self.ZA = 1
                self.ZB = 1
                self.ZC = 0
                self.ZD = 0
                self.ZE = 3
                self.ZF = 0
                self.ZG = 0
                self.ZH = 0
                self.ZI = 1
                self.ZJ = 0
                self.ZK = 0
                self.ZL = 0
                self.ZM = 0
                self.ZN = 0
                self.ZO = 0
                self.ZP = 0
                self.ZQ = 0
                self.ZR = 0
                self.ZS = 0
                self.ZT = 0
                self.ZU = 0
                self.ZV = 0
                self.ZW = 0
                self.ZX = 0
                self.ZY = 0
                self.ZZ = 0

        class FrequencyLetters:
            def __init__(self):
                ''' Letter Frequency per 10000 letters,
                from a 3.2 million character sample size of english novels'''
                self.A = 821
                self.B = 150
                self.C = 230
                self.D = 479
                self.E = 1237
                self.F = 225
                self.G = 208
                self.H = 645
                self.I = 676
                self.J = 18
                self.K = 87
                self.L = 393
                self.M = 254
                self.N = 705
                self.O = 767
                self.P = 163
                self.Q = 9
                self.R = 550
                self.S = 617
                self.T = 921
                self.U = 291
                self.V = 87
                self.W = 254
                self.X = 13
                self.Y = 195
                self.Z = 6

        class ScoreDiagrams:
            def __init__(self):
                ''' A scoring system based on the probability that a diagram will appear '''

                self.AA = -8
                self.AB = 1
                self.AC = 2
                self.AD = 1
                self.AE = -8
                self.AF = -1
                self.AG = 0
                self.AH = - 7
                self.AI =- 1
                self.AJ = - 2
                self.AK = 2
                self.AL = 2
                self.AM = 1
                self.AN = 3
                self.AO= - 8
                self.AP =1
                self.AQ = - 1
                self.AR = 1
                self.AS = 2
                self.AT = 1
                self.AU = - 3
                self.AV = 3
                self.AW = -1
                self.AX= - 2
                self.AY =1
                self.AZ = 2

                self.BA = 0
                self.BB =- 2
                self.BC=- 8
                self.BD=- 8
                self.BE=3
                self.BF = - 8
                self.BG =- 8
                self.BH =- 8
                self.BI =- 1
                self.BJ =3
                self.BK = - 8
                self.BL = 3
                self.BM = - 6
                self.BN = - 8
                self.BO =1
                self.BP =- 8
                self.BQ =- 8
                self.BR = 1
                self.BS = - 4
                self.BT = - 7
                self.BU = 5
                self.BV = - 8
                self.BW = - 8
                self.BX = - 8
                self.BY = 4
                self.BZ = - 8

                self.CA = 1
                self.CB = - 8
                self.CC= - 1
                self.CD = - 8
                self.CE = 1
                self.CF = - 8
                self.CG =- 8
                self.CH =3
                self.CI =-1
                self.CJ =-8
                self.CK =6
                self.CL =0
                self.CM =- 8
                self.CN =- 8
                self.CO =3
                self.CP= - 8
                self.CQ = 3
                self.CR =0
                self.CS = - 8
                self.CT = - 1
                self.CU =0
                self.CV = - 8
                self.CW= - 8
                self.CX= - 8
                self.CY= - 4
                self.CZ = - 2

                self.DA=1
                self.DB=3
                self.DC=0
                self.DD=- 2
                self.DE=0
                self.DF=0
                self.DG=- 1
                self.DH= - 1
                self.DI=1
                self.DJ=3
                self.DK=- 3
                self.DL= - 1
                self.DM=0
                self.DN=- 2
                self.DO=0
                self.DP=- 1
                self.DQ=0
                self.DR=- 2
                self.DS=0
                self.DT=1
                self.DU= - 1
                self.DV= - 2
                self.DW=1
                self.DX=- 8
                self.DY =0
                self.DZ=- 8

                self.EA=0
                self.EB=1
                self.EC=1
                self.ED=2
                self.EE=- 3
                self.EF=0
                self.EG=- 2
                self.EH=- 3
                self.EI=- 2
                self.EJ=0
                self.EK=- 2
                self.EL=0
                self.EM=1
                self.EN=1
                self.EO=- 3
                self.EP=1
                self.EQ=2
                self.ER=3
                self.ES=1
                self.ET=- 1
                self.EU=- 5
                self.EV=2
                self.EW=1
                self.EX=5
                self.EY=0
                self.EZ=- 1

                self.FA = 1
                self.FB = - 1
                self.FC = - 2
                self.FD = - 5
                self.FE = - 1
                self.FF = 2
                self.FG = - 4
                self.FH = - 2
                self.FI = 1
                self.FJ = 1
                self.FK = - 7
                self.FL = 0
                self.FM = 0
                self.FN = - 8
                self.FO = 2
                self.FP = - 1
                self.FQ = - 3
                self.FR = 1
                self.FS = - 3
                self.FT = 2
                self.FU = 1
                self.FV = - 4
                self.FW = - 1
                self.FX = - 8
                self.FY = - 2
                self.FZ = - 6

                self.GA = 1
                self.GB = 0
                self.GC = - 3
                self.GD = - 5
                self.GE = 0
                self.GF = - 1
                self.GG = 0
                self.GH = 3
                self.GI = 1
                self.GJ = 1
                self.GK = - 7
                self.GL = 0
                self.GM = - 2
                self.GN = - 4
                self.GO = 1
                self.GP = - 3
                self.GQ = - 3
                self.GR = 0
                self.GS = - 1
                self.GT = - 1
                self.GU = 1
                self.GV = - 4
                self.GW = 0
                self.GX = - 8
                self.GY = - 4
                self.GZ = - 8

                self.HA = 2
                self.HB = - 5
                self.HC = - 7
                self.HD = - 8
                self.HE = 4
                self.HF = - 6
                self.HG = - 8
                self.HH = - 5
                self.HI = 2
                self.HJ = - 3
                self.HK = - 8
                self.HL = - 8
                self.HM = - 5
                self.HN = - 8
                self.HO = 0
                self.HP = - 6
                self.HQ = - 5
                self.HR = - 4
                self.HS = - 6
                self.HT = - 2
                self.HU = - 2
                self.HV = - 8
                self.HW = - 4
                self.HX = - 8
                self.HY = - 3
                self.HZ = - 8

                self.IA = - 5
                self.IB = - 2
                self.IC = 2
                self.ID = 0
                self.IE = - 4
                self.IF = 0
                self.IG = 2
                self.IH = - 6
                self.II = - 8
                self.IJ = - 1
                self.IK = 1
                self.IL = 1
                self.IM = 2
                self.IN = 4
                self.IO = - 2
                self.IP = - 2
                self.IQ = - 2
                self.IR = - 1
                self.IS = 2
                self.IT = 1
                self.IU = - 8
                self.IV = 3
                self.IW = - 2
                self.IX = 2
                self.IY = - 8
                self.IZ = 5

                self.JA = 1
                self.JB = - 8
                self.JC = - 8
                self.JD = - 8
                self.JE = 0
                self.JF = - 8
                self.JG = - 8
                self.JH = - 8
                self.JI = 2
                self.JJ = - 5
                self.JK = - 8
                self.JL = - 8
                self.JM = - 8
                self.JN = - 8
                self.JO = 2
                self.JP = - 8
                self.JQ = - 8
                self.JR = - 8
                self.JS = - 8
                self.JT = - 8
                self.JU = 8
                self.JV = - 8
                self.JW = - 8
                self.JX = - 8
                self.JY = - 8
                self.JZ = - 8

                self.KA = 0
                self.KB = 0
                self.KC = - 4
                self.KD = - 6
                self.KE = 3
                self.KF = - 1
                self.KG = - 6
                self.KH = - 3
                self.KI = 3
                self.KJ = 0
                self.KK = - 8
                self.KL = - 2
                self.KM = - 3
                self.KN = 1
                self.KO = - 1
                self.KP = - 4
                self.KQ = - 2
                self.KR = - 7
                self.KS = 0
                self.KT = - 2
                self.KU = - 3
                self.KV = - 7
                self.KW = 0
                self.KX = - 8
                self.KY = 0
                self.KZ = - 8

                self.LA = 1
                self.LB = - 2
                self.LC = - 4
                self.LD = 2
                self.LE = 1
                self.LF = 0
                self.LG = - 5
                self.LH = - 5
                self.LI = 2
                self.LJ = - 3
                self.LK = 0
                self.LL = 4
                self.LM = - 3
                self.LN = - 7
                self.LO = 1
                self.LP = - 2
                self.LQ = - 3
                self.LR = - 6
                self.LS = - 2
                self.LT = - 3
                self.LU = - 1
                self.LV = - 1
                self.LW = - 2
                self.LX = - 8
                self.LY = 4
                self.LZ = 1

                self.MA = 2
                self.MB = 2
                self.MC = - 5
                self.MD = - 8
                self.ME = 2
                self.MF = - 3
                self.MG = - 6
                self.MH = - 5
                self.MI = 1
                self.MJ = - 1
                self.MK = - 7
                self.ML = - 6
                self.MM = - 1
                self.MN = - 7
                self.MO = 1
                self.MP = 3
                self.MQ = - 4
                self.MR = - 4
                self.MS = - 1
                self.MT = - 3
                self.MU = 0
                self.MV = - 8
                self.MW = - 2
                self.MX = - 8
                self.MY = 4
                self.MZ = - 8

                self.NA = - 1
                self.NB = - 1
                self.NC = 1
                self.ND = 4
                self.NE = - 1
                self.NF = - 2
                self.NG = 5
                self.NH = - 3
                self.NI = - 1
                self.NJ = 1
                self.NK = 1
                self.NL = - 3
                self.NM = - 3
                self.NN = - 5
                self.NO = 0
                self.NP = - 3
                self.NQ = 1
                self.NR = - 8
                self.NS = - 1
                self.NT = 1
                self.NU = - 4
                self.NV = - 3
                self.NW = - 1
                self.NX = - 3
                self.NY = - 1
                self.NZ = - 3

                self.OA =- 4
                self.OB =0
                self.OC =- 1
                self.OD =- 2
                self.OE =- 8
                self.OF =4
                self.OG =- 2
                self.OH =- 4
                self.OI =- 4
                self.OJ =- 1
                self.OK =2
                self.OL =0
                self.OM =3
                self.ON =2
                self.OO =- 1
                self.OP =1
                self.OQ =- 2
                self.OR =2
                self.OS =- 2
                self.OT =- 1
                self.OU =5
                self.OV =2
                self.OW =3
                self.OX =- 2
                self.OY =- 3
                self.OZ = 0

                self.PA = 2
                self.PB = - 4
                self.PC = - 7
                self.PD = - 8
                self.PE = 1
                self.PF = - 5
                self.PG = - 8
                self.PH = - 3
                self.PI = 0
                self.PJ = - 3
                self.PK = - 8
                self.PL = 3
                self.PM = - 5
                self.PN = - 8
                self.PO = 2
                self.PP = 4
                self.PQ = - 4
                self.PR = 2
                self.PS = - 2
                self.PT = - 1
                self.PU = 1
                self.PV = - 8
                self.PW = - 3
                self.PX = - 8
                self.PY = - 3
                self.PZ = - 8

                self.QA = - 8
                self.QB = - 8
                self.QC = - 8
                self.QD = - 8
                self.QE = - 8
                self.QF = - 8
                self.QG = - 8
                self.QH = - 8
                self.QI = - 8
                self.QJ = - 8
                self.QK = - 8
                self.QL = - 8
                self.QM = - 8
                self.QN = - 8
                self.QO = - 8
                self.QP = - 8
                self.QQ = - 8
                self.QR = - 8
                self.QS = - 8
                self.QT = - 8
                self.QU = 8
                self.QV = - 8
                self.QW = - 8
                self.QX = - 8
                self.QY = - 8
                self.QZ = - 8

                self.RA =0
                self.RB =- 1
                self.RC =- 1
                self.RD =- 1
                self.RE =2
                self.RF =- 1
                self.RG =0
                self.RH =- 3
                self.RI =1
                self.RJ =0
                self.RK =1
                self.RL =- 2
                self.RM =0
                self.RN =- 2
                self.RO =1
                self.RP =- 1
                self.RQ =0
                self.RR =- 2
                self.RS =0
                self.RT =- 1
                self.RU =- 1
                self.RV =0
                self.RW =- 1
                self.RX =- 3
                self.RY =2
                self.RZ =- 8

                self.SA =1
                self.SB =1
                self.SC =0
                self.SD =- 4
                self.SE =0
                self.SF =- 1
                self.SG =- 3
                self.SH =1
                self.SI =0
                self.SJ =1
                self.SK =0
                self.SL =- 2
                self.SM =- 1
                self.SN =- 4
                self.SO =1
                self.SP =2
                self.SQ =3
                self.SR =- 6
                self.SS =0
                self.ST =2
                self.SU =0
                self.SV =- 3
                self.SW =1
                self.SX =- 8
                self.SY =- 3
                self.SZ =0

                self.TA = - 1
                self.TB = - 1
                self.TC = - 2
                self.TD = - 5
                self.TE = - 1
                self.TF = - 3
                self.TG = - 5
                self.TH = 5
                self.TI = 1
                self.TJ = 0
                self.TK = - 4
                self.TL = - 2
                self.TM = - 2
                self.TN = - 6
                self.TO = 1
                self.TP = - 4
                self.TQ = - 2
                self.TR = - 2
                self.TS = - 2
                self.TT = - 1
                self.TU = - 1
                self.TV = - 7
                self.TW = 1
                self.TX = - 8
                self.TY = 0
                self.TZ = - 5

                self.UA = - 4
                self.UB = 0
                self.UC = 2
                self.UD = - 2
                self.UE = - 5
                self.UF = - 3
                self.UG = 2
                self.UH = - 7
                self.UI = - 3
                self.UJ = - 3
                self.UK = - 2
                self.UL = 3
                self.UM = 0
                self.UN = 2
                self.UO = - 8
                self.UP = 4
                self.UQ = - 6
                self.UR = 3
                self.US = 2
                self.UT = 2
                self.UU = - 8
                self.UV = - 5
                self.UW = - 3
                self.UX = - 4
                self.UY = - 7
                self.UZ = 2

                self.VA = - 1
                self.VB = - 8
                self.VC = - 8
                self.VD = - 8
                self.VE = 5
                self.VF = - 8
                self.VG = - 8
                self.VH = - 8
                self.VI = 2
                self.VJ = - 8
                self.VK = - 8
                self.VL = - 8
                self.VM = - 8
                self.VN = - 8
                self.VO = - 1
                self.VP = - 8
                self.VQ = - 8
                self.VR = - 8
                self.VS = - 8
                self.VT = - 8
                self.VU = - 8
                self.VV = - 8
                self.VW = - 8
                self.VX = - 8
                self.VY = - 3
                self.VZ = - 8

                self.WA = 3
                self.WB = - 4
                self.WC = - 5
                self.WD = - 6
                self.WE = 1
                self.WF = - 5
                self.WG = - 8
                self.WH = 3
                self.WI = 2
                self.WJ = - 2
                self.WK = - 6
                self.WL = - 5
                self.WM = - 4
                self.WN = - 1
                self.WO = 1
                self.WP = - 6
                self.WQ = - 6
                self.WR = - 5
                self.WS = - 4
                self.WT = - 5
                self.WU = - 7
                self.WV = - 7
                self.WW = - 3
                self.WX = - 8
                self.WY = - 4
                self.WZ = - 4

                self.XA = 0
                self.XB = - 4
                self.XC = 5
                self.XD = - 7
                self.XE = - 1
                self.XF = - 3
                self.XG = - 8
                self.XH = - 2
                self.XI = 2
                self.XJ = - 8
                self.XK = - 8
                self.XL = - 8
                self.XM = - 3
                self.XN = - 8
                self.XO = - 5
                self.XP = 7
                self.XQ = 4
                self.XR = - 8
                self.XS = - 5
                self.XT = 2
                self.XU = - 3
                self.XV = 0
                self.XW = - 3
                self.XX = 6
                self.XY = - 2
                self.XZ = - 8

                self.YA = 0
                self.YB = 3
                self.YC = 1
                self.YD = - 1
                self.YE = - 2
                self.YF = 1
                self.YG = - 1
                self.YH = - 1
                self.YI = 0
                self.YJ = 3
                self.YK = - 2
                self.YL = - 2
                self.YM = 1
                self.YN = - 4
                self.YO = 3
                self.YP = 0
                self.YQ = 1
                self.YR = - 3
                self.YS = 1
                self.YT = 0
                self.YU = - 4
                self.YV = - 1
                self.YW = 2
                self.YX = - 8
                self.YY = - 2
                self.YZ = - 8

                self.ZA = 1
                self.ZB = 4
                self.ZC = - 7
                self.ZD = - 7
                self.ZE = 4
                self.ZF = - 7
                self.ZG = - 5
                self.ZH = - 6
                self.ZI = 1
                self.ZJ = - 4
                self.ZK = 0
                self.ZL = 0
                self.ZM = - 5
                self.ZN = - 8
                self.ZO = - 1
                self.ZP = - 5
                self.ZQ = - 8
                self.ZR = - 8
                self.ZS = - 8
                self.ZT = - 7
                self.ZU = - 6
                self.ZV = - 8
                self.ZW = - 8
                self.ZX = - 8
                self.ZY = 2
                self.ZZ = 8

        def get_average_probability(self, a, b):
            scores = []

            for each_column in self.cipher_columns:

                # If the cipher requires padding disregard the last column
                if len(each_column) != len(self.cipher_columns[0]):
                    break

                letter_a = each_column[a]
                letter_b = each_column[b]
                collective_score = self.get_collective_score(letter_a, letter_b)
                scores.append(collective_score)

            ave_score = reduce(lambda x, y: x+y, scores) / len(scores)
            return ave_score

        def get_collective_score(self, a, b,):
            # frequencyDiagrams = self.FrequencyDiagrams()
            # frequencyLetters = self.FrequencyLetters()
            # prob = (getattr(frequencyDiagrams, a + b))
            # a_prob = (getattr(frequencyLetters, a) / 10000)
            # b_prob = (getattr(frequencyLetters, b) / 10000)
            # individual_prob = (a_prob * b_prob) * 10000
            # colective_probability = individual_prob / prob

            scoreDiagrams = self.ScoreDiagrams()
            score = getattr(scoreDiagrams, (a+b))
            return score

if __name__ == '__main__':
        plain_text = '''So my story starts on what was a normal day taking calls on the front line for a large cable company. The job pays well and for the most part the people I deal with are fairly nice to talk to.
Quite often we'll get calls from seniors (especially in the morning) who have premise equipment issues such as "snow on screen" or "no signal" on their TV sets connected to our digital equipment.
Now my heart does go out to some of these folk because up until recently (past few years) we would supply straight analog cable to many homes (coax direct from wall to TV with scrolling guide). However most cities we service nowadays require our digital equipment to receive channels, and this has caused a lot of frustration with older people who don't know how to operate said equipment (ie. always having your TV set on "video" or "hdmi" to get picture). So often times we get customers who are repeat offenders with long ticket histories of these types of issues.
So anyway, I get a call from an older gentleman who's quite bitter and mean right off the bat (doesn't like that I asked for his address / telephone number to verify the account, hates that he has to speak with a machine before reaching an agent, etc.). I have some experience handling these types of customers, however this call was going to be a little different.
I spent over 45 minutes with this guy (we'll call him Mr. Smith) trying to get his TV set connected to the digital box properly so he could receive a picture. No luck. He was getting clearly frustrated by the whole ordeal and started blaming me for not being able to do my job properly, how I was useless, etc.
Whatever.
Like I said, I've dealt with this before so I tried my best not to take it personally, but eventually I had to ask him if we could book a service tech to the home (a courtesy call) to get his TV working correctly. Unfortunately, our booking calendar was showing an appointment 3 days out. That's when he dropped this on me:
"Don't bother sending a goddamn technician, because I'll be dead by then. I'm 94 and TV is the only thing I have left, are you really going to make me wait for a tech?"
I instantly felt bad. I mean, I've heard every complaint in the book as to why people don't want to wait for a tech but this one kind of got to me. I'm in my mid-20's so honestly I can't even imagine how it must feel to utter those words.
So I spoke with my supervisor, who said they'd see if we could get someone out earlier...but we couldn't promise anything. So I let Mr. Smith know and he was predictably not very happy with my answer.
At that point it almost sounded like he started to cry and went into how he has no family left, and no friends that come visit (this was after I asked if there was anyone in his building that might be able to help). Man. I felt terrible, so I took it upon myself to ask Mr. Smith if I could pay a visit (he lived in a small city over from where I was, not very far to drive).
He was a little shocked I was willing to do this, but sounded thankful I was willing to come out and help him personally.
So I head over, get to the residence and meet him - within 30 seconds I had the cable running again (simple input change) and even brought him a simplified remote for his set top box to avoid this problem in the future.
That's when he started crying. He goes into how he hasn't actually spoken or really interacted with anyone for years. He gave me a hug and told me how thankful he was that I came out and helped him, and told me how sorry he was for being so mean earlier on. I said it was no problem and I was happy to help, and that was it - I left.
3 weeks later, my supervisor comes to my desk and asks me if I could come speak with her for a bit about an account for "Mr. Smith". Turns out, he sent the cable company a letter outlining how thankful he was for helping him with his issue and how it really "made an old man happy again for once in a very long time". The letter was framed and put on our front entrance to retail.
I guess the moral of this story is no matter how nasty someone is to you over the phone, sometimes they're not always a terrible person and just going through a lot. I still think about Mr. Smith occasionally when I get those nasty customers and it makes me feel a little better.
Anyway thanks for reading just thought I'd share how this one call changed my outlook on life :)'''
        cipher_text = '''
KIWDY FAIAS YQXQF GMQDZ OHUQK NEFVL
AZPZP CXYDJ QLVGC KXPAS IENMN JYNGA
ODJPJ YNTCF RJUIT ECGGS PVEAB STKTN
BJOHZ OKDHA SGHPR LAEFU OSKRW ANNLG
RTZTT KPYAB QGLQH FVDTQ QORNB ZDOCR
SMQVV QXYVC QNVNE BXKAJ HHBWJ TPVMV
FEQXQ QKAWP EHVQF GMVPU OSGGG KAKYQ
NARZM AKIOS PBZSG KCWWW PPNBE MQMBB
ZMCHZ QSJRW RWPEZ RTCFT ANBOH XBSMC
KJNNT COGCK ZDSWI KIPWG PUYMN NCLXD
MAXNN HLWEC KCAWH IVLNW AORGA CTWQP
HKHRI PRWRZ RNSYQ XQFGM QDZOH ZSKDH
NEGQH ZPNPF VTHCF ENWXM JXYAA SHBMS
YWRUA PAEZM WCMRP PEZEC AGSBF VLQQT
KSNZE REBSL HVBYA WQVSM GEJOW SOKDG
MEREX SKDHT JHQQP QTNNS QTSSJ SBQJL
RTLSN KPVQA XSAIA FVLET RFIPA GWYYV
UMVNG QASVK PQKIQ XQAGX HAZIM XAOAF
PVGHX SKRUW WDMXR ADBPG SEBFM QNFEW
PQVOT ANESN RRRGC WHWHZ CFANK IWBQT
KDAPW XRMPV NWVDQ TSZSA UVBWB SYQTK
PEZNO ZTTNX ZSRNZ TYGRJ HEUCV RAPJN
SSPXH JQZSR WBZJG SBOAB ZOGGI EOHEQ
KBJHY HWYCO NWLZX MXRPN WBYAW QVKJN
BYQSK RRNKP GDNSY GYGRJ HEUCV RTFSO
WSOKD GMDGU QCFTA RWEIO MKAPI VVMVR
NLCDL GYQVO APAEZ NPSGS LPWXM XSGYU
PVGHH KRRTX GOWGL NLASY VIQQG QNBJS
VAMKD AUGPT NZTBH QZXTQ BSQJS JQXYC
OGHAZ IMXAA HLIGO SWBZJ GSEZN TCFNL
BYSZQ PQMVP YJZGL KSNBY AWQVL SIMWH
RTNHR TPGPD XOABW PYQNW CFAPF CGIJZ
ASQXQ WQZCF APVVW MTBET MHZPH GCLQH
FSTSS GFNLO EZRXZ OJGPS SEXSG YUPVX
EWXAP HQSPD XOAQE FQVNW CFAPF CGIJZ
ASAVE ZNPSG SLPEZ RXZON KPGZR MXKSA
FEOIJ ZSKHX SQXYV ASHNV OKGJN TGLEZ
RXZSP VZZUN JZKVH KIWQX BONEP VQMZC
RIHEM QSKRG QAIUA SGPZM VFELM HZOQQ
LYUMH XAPHQ WXSBP AHLIG OSWBZ JGSYV
QSZWY MNJDS KBOMV PSQRX RWNPK ZDVTX
RRKFC VNYVM YWVWX EUCFN AKYQN ARZMT
VMVYK BPNNV CWKYA KJGLS PPQVA SWFVL
EAXRR UPGQA SYOGH AZIMX AOGHF SDVAX
OTGLW XBYVU RELJD QARGS AKIOS XSKQN
FEWPQ VOTAK GENLI SMRPL OVZRO GHVXL
QYQKT PNEDD YTADQ KLOHT POWHW GPUQL
ENLFM DNXSK DHNSS EORKY EFEZN ABOTL
FQHNY AASTB FGSKB SMGEJ QBCRZ RNPDP
BQUHN WKSQX GAGDI IUWHX LANAL WQTSQ
CTZRJ EQQXA PHQSP DXSRN HNVDS QBURZ
WWRNW AAZZN PWMTC FANDY DNXSK QNFEW
PQVOT APYDA XPHDG TJUNP BJQHK IWBQT
KDAPW XRTIW WHQXG UGALW MPCTS KQKNQ
XYVQS LLVQX ZUIQM MMVQJ WYGTL QQEZV
MXNEL NBGWN KBHYH LSQEN RGSGL GOHOP
WYWVH WBXNA ZNBJL MHZOQ QKZDN YAMMG
MZSYS CFNWP KOPMJ KQGMS QRXRW NPKSQ
XYCGD HHZKN JNORR PEHVQ MJMJL HHERB
EKHKI WNZAK SNNYV SWZXO QXEPD GVUAP
NVXMT ZONAP AENTG KRZPP WHXAK ALBWX
TKZXG ENRZS KBHYH LCTRP GLJHL EUVXO
LMVFS NRJJO RNFQA BSMGW QHZQA UPRNK
PVPHQ PQMVP UZRMX KSQLR QXQVO GHXEO
SQFKS NKIOS TPZNG MEZNQ TKSNX JYNWS
GYUPV DMZXR RRFCV AXQJN RIEJR TVAMR
PHHER RU
        '''
        # plain_text = ''.join([x for x in plain_text if x.isalpha()])
        cipher_text = ''.join([x for x in cipher_text if x.isalpha()])
        # chiSquare = ChiSquare(plain_text)
        # print(chiSquare.ic)
        # print(chiSquare.ic_difference)
        cipher_2 = ''.join([x for x in '''
COOUS ULYDU TQOHY SEELP EUTST GTOAR
IDTHM WPEER DTTEF EXUTO ROSEC UYCOU
DUBEU LUONL IKFTE YHCER LROTU ESAOF
ANRAI EQSOR ETLER HTFTE UISEI SDQBY
LSFOS ERTIN NRGED AWTOR KLEQA IASNT
RFEXL OASMP TBOTW UHEER ISTWD EOIUL
ETASV LTAGI UYAST OTEAR PNOIN GNITI
HOEDY TETCR OTNQT IUPES ROKEY MNTLA
ITNKS HIITI OHNLC EYTDE ANNDH TREIG
ITNGO HTTOD OONAH DTTET LMLIO IOENS
LDLAO ORFSY DMEFS ARUOM ILNGO LEENR
OSCKO TBNEF HEECA TORMP EYCLD DANRE
KARUY NPBTC UONDC FSTSU EANRM SOHNE
YLEEN OTPRA IIOND TFSUN RNEAH DCAHT
ETNET BFAIT OEMPS CAHNY LMOYW PEEES
OOSTI LTHHE TRIRN EERME VSINN AGTSA
OPVIE RDDER FITOI ELLOW MCECU OONNS
SEINI RCMAL NOIAC RWFHO ANFFT TOARD
YPTHE AEOIR GEYBS RINLL VIESI NTIED
UYRCA OONMP EYCAI BUNSE IEEVN LEBDI
ONNAT RNEDI NFANL ICSIA TTEMS AESNT
NAOTK MSIEE TNORV GEICO YRLON MSETI
TEMEU SNVTB OIBEV DLTIE ATTYE HOEUR
OPYEE LEMSD VEEMA RUSCH RTTHY EEFIR
SAOFD RHEAR KOMAG RKWIN ONNAO RNEDY
CRHIW IKUNO WOILV ULYNE ERADS RTEHI
IMLAO ANEDC NLTBT DEUBO EEDWI RIHTH
TBUNS ULTES AOREL UWYIL TNOHY GAIVE
NUAMD REOGO IWNAI NMOER HAISY NTCOR
NSEOS OFAIT SOEBN RUWSI CSRIA SMEIN
OSUHA YALVE NHCET ANCOW GRHTG IAONE
IEOUO GSRWR NGDEH IENDW YLOUT ENIET
EDLLR WOEVE LMLIA IOANM FYENS ORNON
LMOYW PEEES FRINI EAENC YLDET LVAAS
DTWHH EEANT MCPAE ONEYD RLEDK ABCAN
TUCYT PARND REREE ITHIR TEPLW NAMNS
WRIPU EEEDO DAENM NRTON ADNAO ESATR
IOCAO MLNPR DIURT TIFNG AELIN CFHOR
NAERR EGIYC SSLAE ISITY SRARL AEASU
ETRET HATRE SOANF UDHSO SOUMW NECRS
ROEUL ANHAB PTAYI OTEHE SBICR AERNE
IYLLD BSGAN LHART EGTES LTITT IYUIN
TEATB SEHIS RNUPE KTATH YEORM WKNTI
ESPOD RRETE THYOL AUTSO LMLIO IODNW
OTFEN HNRRO CTKWE OHSIL RGESE GSAIV
RYGIH UNLGT MCPAE ONEYS OPYEO LEMST
PEBUG EYKIN OTNAH DTIET OSNET MYITO
UENDT FSHSE OPHEE TLUPR RATHV IEPLI
FSTHA OOESE IECAU RNMSH YTENS BRRON
ENRHE DAUND DANEI NFDAR DUEAG SLOIN
HOERE TWSIS WOILV ULYHA SLTAE OLELR
CPTFM ERSOM DNECH YEANT WRORG DKAIN
TNRUN DSATI EARIS MCGAN HFOMT WYOOU
AODVA KAONT AEYGA MOGDH EERCY MYVON
SUOUN RLOSI EELYI RCCHR ATNWN ICSHU''' if x.isalpha()])
        ze_cipher_text = ''.join([x for x in ''''
t i f a t p o k g r i a n
eb s t m n e l r t i a e
t c t n i s h s e s i n i
d f e n a h m e u s t v o
o e e m a t r l t a s l s
l i e p t n y l e t a h k
s s r g e a t u n s t t i
h o o t o p e o t w e b s
r t l i r e s f e e t o h
e e w h c e l p t p n o s
b t l a a l f e s o a n i
t k i a r d f c o n e o c
e e s c r nozo r a o n
v l i i u t e h f m e g y
e e e z s f r h i a o t s
o t t m t e a i s h r h i
n o i a n l h h s g d t u
w a i a t y p e s ma y r
o i o y o t r s l f u s b
f h e r e r ecosoaf
m l t u e n a b h r a a e
h b a t v m n l t n e e u
d f e s e t t o t c e r i
e s s g i t h n g t s o u
s i o r e c l n e u e u v
o f i l d m s e l d f b u
r d t r i s i e e r ezt
t l o e a n t p n t s l a
r i t e o n r df f eof
n u t w o e i o o h w m r'''.upper() if x.isalpha()])
        vigenere_cipher = ''.join([x for x in '''
        ZSXNZXZGFWEPYXDDUASPAALHHRZGTEWSHCEPRMYVJEWAZSYIOIQGVREAPRPUVVLAHVRTJEMALGZBWEYNALPYVFAPFWHT
        SPLCKJZGALPBVWEEHVEIOIATVTWTPHPPSATIOECTMETGSCYXJIEDAEWZASBJPXPDMXPCDIWANIERHPWHMVZBZIYXVVDT
        ZTPRPEWAFMYIOIXDYRTCNASDOEGTWVPBPWPTXYTETIYIPWDJLWDJJLLHZRZLVRDRYIPCVVYDZMRCHPZCALPXYXGHLXDR
        VRYTJXPSASZJYHTVPXLALUFXWQPCARZLTCSTHVESVIDVVSFIASDDTIZUALPHLJZARFPRHYDTBTFCAMWGLGPCAPJEHWEU
        LAJTHVDLLAZJSHDJWTWNZXCPPKSIHRLAVKNPIPPIVQLCFLZBLWNDHBOXYINIMVZBDEWAASEKDMEWZGCDSPTCNKFXKISD
        DIGTYQZHAGTIPIDLLWPGCMNTUSHPKEJHYIBJPVPDBVOXNMEPSIBJPTXTUXEDYINTPZPROEYCLPDPUHEWPWSPZGLJZIOP
        SSEDMJCJZXCPAMZCDMEWVPOTYTPDWPPLOSODUXVCVASDDXZDWICPAIDPPHPFBMABLREXLEWLHCDWHZTCNCZJYXGHLXZC
        CMOTVSCWKQTIVKPIWMNIBVPHVSQILREXTIDLLKPIJYDIVQPGZASDHVPGLTPPASQULROTYWHXALWDUKEXJOPIOMDIVVTT
        ZSQIOIDTACATZSQXZWFTZWZPUCHPFMRTAENPSPQGVQLCVPOTYKPCAPPBHRHWVWBJPXPQPXETYEYSTILCYMRWASQUALPQ
        HXODLWYISMVTALLIPEDZLHQDYLTHHHOGLWDILPPEOSYTUYXQLVEDCICXMCEWLENRVYYIOEETZXSPALPWHWEDZTPPRATI
        OEXPJLTCLFPUVVPGLENWPRRPUERTUXPIJMSPCIDDTIPMWICXLRNTOEYSSMYVALPHLXJELWZUJYDIVQPGZLZLLZPGALTH
        JEWADEDVVMYVASMTHPTIAPPSPJQTYIYIPWATUXZKLVXXUYETZATIOXSXZKFNDIWAJEWAOMXBYWXXALEGFMYVASRTALTH
        AZDTAGZCUINILHEDALPSPKTIHPMDETCDWICAFWZWLGZJSHCTJITKLEAXJXFGLRZABGVWLALHNIEIPRRRSILGSCQGBWEG
        HXPSICEWLASDSIZGKILAHROHAECILHMAHQTCNQPUVVYDAFPXUKLQSIEDKSXNQSMEYSATYPJWVATLHWFHLPPHZIERDLLI
        LZPGSMVTPWLXKMGTKILAAATIOXSXZFPUVVPHVMEGPIOBFFPHARZIASEPRITIWICHVRLASCMJAIGTUXFPSPJXOEOIVEDZ
        OMXXMAPRVYWSISZZHWPGCMNTAINWASEWLLZBLENDBVETZCNPSPEDNIEWPWEKDSCZPRRRVVCTJXWNBRQDYXFCHXPAFSFG
        ISZZPRRRHPPCKECLHWDWVATCNEYPWTZXUXXTUXOPFWZJAXSPAWHWLRSTKVZEWIOIOMDDUQPSVREQVXSTYWPCKMYVHKZS
        KEXCAINWUMNXHRMTJEFHLMWAIIOTHHMNALPCPQLCKXGXZXSTVRWNALTCNMSPCIWTMXLGLCZJYILASCRDPRRIVQLZLQPL
        HMEUVVLILGSXPRDIHREAFJPAAFLSPQPPUMGTOILGKIGTYCNDTTWPPREXUXSTISZZHWEDDLJELSAALHZCAALCAXZLHMEU
        VVLILGSQBXEWPWZCLOTCKSQVVXEDTITBPRXNTMOHZSSDUIDISCTRHRETCIYXTERXUISDDMEBBWEULIWIVYEILVEWVWPL
        VVOHZSTHWSVTDMEWTCDJWICKPWZGDLZHHMOIOIJSZIPXMAPRVYWSNIEHVQPDUIZJAILGSMPGIYELLGZJSHYIWVZBPWPP
        UCEWPRRHVMWTAQCHTMEWRRZLHROWLALHWVPSPGEPIPJCVXGTYCSPWTJLPXSBFEYHDICPAXSPATZXUXTIHPXDZXDDBROT
        KPTZLLPHAECILHEDJVJPUHHTUXTCASSDDLPWHWYDMEXXSCWTMXLCKRZUYMPCKWEWHXNDTIGXZMEIOMDLHWLUAICXHWVT
        KMQIOICTDEDPUCZCLMYWPWMJPPOXUKEWHXXXNLEQLEMALXZWLPABHRTULPEILVCXIPPHVMEDVOTIBTZCTCDTSJEDHWVB
        YWXXALTUPGZJSHAPFEGXZMEWLPTKLHTCHWXPSPNXACZKLVQGVQHWLVPXDEDCVXGTYCQPYXZSYMGTOIHPZEWXAXWTZLZR
        RIOXDEDLPPWXUKEDKSEWPWMJAWZJUHPSALLCRJFAPALHDMWAPRRIVGZBLSFIHROWLPAWPQATYWZCHPWNZSTWLEODCICV
        LXEDALPGLWTSLRNTHROBLIEWPQHXALTCZINDUHDXOEOIOINPIPPGBRYXUKLVHMYHPQAALMYEBXNWHRRTHROTCIYQYSFV
        OXSXTEDXTTWXMMPSYIXDAIQDYLTHZIEIVTMDEXZPCSTSALTHWVZQSIXXUXSTMYEJYIEWHXDLOIYWLWEPYXPSJVJXUKST
        NSPHPREDOSHWLLLHUXLRAYLASCDEVOPCVVCTHPWNPRETYENILHHXALLCFSYTMSCNLECHOIRPCIXTHLFVHROIVPOBLLZL
        ALLCRJFAOIHPZXSPAMNPTIZJAEYSOIWELHSXTEYSASWSTISDDWZGYCSTDEDUVVMTPRRHVQPPUILGSMPGVRTHHMOXAALH
        USAGVFWTTEYSPALHOEAEFXZWLPAPUHEWHXHPZMEXSIQIDIPZZPLILVXNZYATYZTHVVNDTIDIVQJSLWVPUHLHRWXTPJTR
        VYWSJSXTZTPPRATIOLPGMSCPIMEPISFIHRLRJSFCAJZGTVDBPXSIBVYHVYEWLWPCAXSTJEMALGZBWEYNHPPIAICDBXWX
        UMYVOSHIOEYZMYWWLALHMSCWLPAXUKSXTATIOLTHPWDJLEYSOSHXAVPPSPJBHHPPUSWSTEYWHTANHKLXUJZGVRNTPRLK
        LVJAVRRIPQPIOIWTAXPGDEDUYEXTKEYSWYEDUSFGMVZCAIYIYEYRLXZGLXLXSMRJLWDIOIXDYEWDMXSXZWEDYCTHUSXP
        AXPGOSHCHWENZSXTVRPXZXZNVYZKLVEWLTSDUIDDTIEXTIDIOIJGLRZIHPHPFWLILVCXIPPELVDDUEYSQYDINSTCNXSG
        VYRWHPZIPWEXSPEWPRVPISFITVDBPXSDJGLHPSYPSPJLOIYXNIEIOSDTUEDIFGFHASXTYWLCKMEBHOPHTIQTLPLAPXEA
        LFPIAICPUCHPFXSPUODUVVCTHHTCNNFHAXSDBKSIPHDWHVPWVAEWPWZCLGLASGSPUKPSTCZJAPZDRSYAPJP
        ''' if x.isalpha()])

        for each_degree in range(2,30,1):
            print('[+] Running Degree: %d' % each_degree)
            dia = Dia(ze_cipher_text, each_degree)
            dia.permutation()
            dia.run()
            print(dia.key)
            # nth = NthMessage(cipher_text, each_degree)
            # nth.output()


        # dia.run()

