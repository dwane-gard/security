from random import shuffle
import collections
import co_incidence_index



class Trans:
    def __init__(self, cipher_text):

        self.cipher_text = cipher_text
        self.cipher_text = self.cipher_text.replace('\n', '')
        self.cipher_text = self.cipher_text.replace(' ', '')

        self.multiples_list = []
        self.factors(len(self.cipher_text))

        print(self.multiples_list)
    def factors(self, n):
        '''
        Calculates the multiples to create n and prunes duplicates
        '''
        multiples_list = []
        for each in range(n+1):
            for each2 in range(n+1):
                if each * each2 == n:
                    print(each, each2)
                    if each not in multiples_list:
                        multiples_list.append(each)
                    if each2 not in multiples_list:
                        multiples_list.append(each2)
        for each in multiples_list:
            if each not in self.multiples_list:
                self.multiples_list.append(each)
        return multiples_list

    def structured(self):
        x = [x for x in 'COOUSULYDUTQOHYSEELPEUTSTGTOAR']

        return

    def counting_qs(self):
        possible_key_size = self.multiples_list
        print(possible_key_size)

        print([self.cipher_text[i:i+50] for i in range(0, len(cipher_text), 50)])

        # For each key size
        for key_size in self.multiples_list:

            cipher_list_sized = [self.cipher_text[i:i+key_size] for i in range(0, len(cipher_text), key_size)]

            # for each row of cipher text
            for each in cipher_list_sized:

                # reset q and u count
                q, u = 0, 0

                # check the q and u count
                for key, value in (collections.Counter(each).items()):
                    if key == 'Q':
                        q = int(value)
                        # print(q)
                    if key == 'U':
                        u = int(value)
                        # print(u)

                    else:
                        pass
                # if there are more q's then u's this isnt the right key size
                if q > u:
                    try:
                        print(key_size)
                        print(q,u)
                        possible_key_size.remove(key_size)
                    except:
                        pass
                    pass
                else:
                    # print((collections.Counter(each).items()))
                    # print('[possible key_size] %s ' % str(key_size))
                    pass
        print('[Possible Key sizes]')
        print(possible_key_size)


    def brute(self, cipher_text='COOUSULYDUTQOHYSEELPEUTSTGTOARIDTHMWPEERDTTEFEXUTO'):
        f = open('sowpods.txt', 'r').readlines()
        all_keys = [x.upper().replace('\n', '').replace(' ', '') for x in f]

        plain_text = []
        plain_words = []
        cipher_text = [x for x in cipher_text]

        while True:
            for each_key in all_keys:
                ze_line = [x for x in each_key]
                if set(ze_line).issubset(cipher_text):
                    for each in ze_line:
                        print(each)
                        cipher_text.remove(each)
                        plain_text.append(each_key)
            if len(plain_text) > (len(cipher_text)*2/3):
                print(plain_text)
                exit()
            else:
                plain_text = []
                all_keys.remove(plain_text[0])



    def random(self):
        f = open('sowpods.txt', 'r').readlines()
        all_keys = [x.upper().replace('\n', '').replace(' ', '') for x in f]
        shuffled_list = ([x for x in 'COOUSULYDUTQOHYSEELPEUTSTGTOARIDTHMWPEERDTTEFEXUTO'])
        i = 0
        plain_text = ''
        checked_answers = []
        answer = False
        ze_checked_answer = ''
        while answer is False:
            while i < len('COOUSULYDUTQOHYSEELPEUTSTGTOARIDTHMWPEERDTTEFEXUTO'):
                ze_checked_answer += str(i)
                plain_text += shuffled_list[i]
                i += 1
                print(plain_text)
                print('[Testing]')

                if answer is True:
                    exit()
                else:
                    checked_answers.append(ze_checked_answer)
                    pass

        print(plain_text)


cipher_text = '''
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
        SUOUN RLOSI EELYI RCCHR ATNWN ICSHU
        '''

trans = Trans(cipher_text)
# trans.random()
trans.brute()