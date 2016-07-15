import itertools
from functools import reduce
from math import ceil
import time
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

        null_count = 0
        while not (float((null_count + len(self.cipher_text))/(len(key))).is_integer()):
            null_count += 1

        plain_text = [None] * (len(self.cipher_text))
        column_size = int((len(self.cipher_text))/(len(key)))

        cipher_columns = [self.cipher_text[i:i+column_size] for i in range(0, len(self.cipher_text), column_size)]

        for each_key_char in key:

            if null_count > 0:
                cipher_columns[int(each_key_char)-1] = cipher_columns[int(each_key_char)-1][:-1] + '.' + cipher_columns[int(each_key_char)-1][-1:]
                null_count -= 1

        new_column_size = ceil((len(self.cipher_text))/(len(key)))
        cipher_columns = [self.cipher_text[i:i+new_column_size] for i in range(0, len(self.cipher_text), new_column_size)]

        k = len(key)
        j = 0
        for each_key_char in key:
            i = j                                                                   # reset to approroite starting point
            n = int(each_key_char) - 1                                              # Find the correct column
            for each_char in cipher_columns[n]:
                try:
                    plain_text[i] = each_char
                except:
                    pass

                i += k                                                               # Step the key size to find the next characters position
            j += 1                                                                   # Step when moving to the next column
        plain_text = ''.join('.' if x is None else str(x) for x in plain_text)
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
        print(cipher_blocks[0])
        input('derp')
        for each_block in cipher_blocks:
            for each in key:
                    # unencrypt that character and add it to the plain text
                    try:
                        plain_text += each_block[each]
                        print(plain_text)
                        time.sleep(0.001)
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
    test_cipher = "ARESA SOST HEYLO IIAIE PENG DLLTA HTFA TENHM W"
    cipher_2 = '''
COOUSULYDU TQOHYSEELP EUTST GTOAR
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
SUOUN RLOSI EELYI RCCHR ATNWN ICSHU

'''
    test_cipher = ''.join([x for x in test_cipher if x.isalpha()])
    cipher_2 = ''.join([x for x in cipher_2 if x.isalpha()])
    decode = Decode(cipher_2)
    # print(decode.permutation((4,2,5,3,9,8,6,1,7)))
    print(decode.permutation((7,1,5,0,2,3,6,8,9,4)))
    # print(decode.columnar((4,2,5,1,6,3)))
    # print(decode.columnar('POTATO'))

    # multiple anagraminf
