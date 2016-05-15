from random import shuffle
import sqlite3
import functools
import multiprocessing
import collections
import itertools
import co_incidence_index
import time
from string_check import BoyerMoore
from corpus_analysis import Analyse
from math import ceil


single_thread = True
class Trans:
    def __init__(self, cipher_text, key_size):

        self.cipher_text = cipher_text
        self.cipher_text = self.cipher_text.replace('\n', '')
        self.cipher_text = self.cipher_text.replace(' ', '')
        self.multiples_list = self.factors()

        self.key_size = key_size
        # Break the cipher text into blocks equal to the key size
        self.cipher_blocks = [self.cipher_text[i:i+self.key_size] for i in range(0, len(self.cipher_text), self.key_size)]

        print(self.multiples_list)

    def factors(self):
        '''
        Gets the factors of the length of the cipher text
        :return:
        '''
        n = len(self.cipher_text)
        return(list(set(functools.reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))))

    def ze_analyse(self, answer, key):
        '''
        Analyses the calculated answer to determine if it indeed english
        :param answer:
        :param key:
        :return:
        '''
        # ze_analyse = (Analyse(answer))
        # ze_analyse.run()
        word_list = []

        for each_word in open('sowpods.txt', 'r').readlines():
            if len(each_word) > 4:
                each_word = each_word.replace('\n', '')
                if each_word.upper() in answer.upper():
                    word_list.append(each_word)

        words = ''.join(word_list)
        print((len(words)/len(answer)))
        if (len(words)/len(answer)) > 0.5:
            print(len(answer))
            print(len(words))
            print(answer, key)
            with open('results.txt', 'a') as results_file:
                results_file.write("%s | %s | %s\n" % (str(answer), str(key), str(len(words)/(len(answer)))))


    def ze_worker(self, inq, outq):
        '''
        Unused code
        :param inq:
        :param outq:
        :return:
        '''
        self.ze_columnar(inq)

    def ze_columnar(self, key):
        '''
        Decrypts Column Transpositional ciphers
        :param key:
        :return:
        '''

        null_count = 0
        while not (float((null_count + len(self.cipher_text))/(len(key))).is_integer()):
            null_count += 1

        running_answer = [None] * (len(self.cipher_text))
        key = ''.join([str(x) for x in key])
        column_size = int((len(self.cipher_text))/(len(key)))

        cipher_columns = [self.cipher_text[i:i+column_size] for i in range(0, len(self.cipher_text), column_size)]

        for each_key_char in reversed(key):

            if null_count > 0:

                # cipher_columns[each_key_char] = cipher_columns[each_key_char] + 'x'
                print(cipher_columns[int(each_key_char)-1])
                cipher_columns[int(each_key_char)-1] +=('.')

                null_count -= 1

        for each_char in cipher_columns[-1]:
            cipher_columns[-2] += each_char
        cipher_columns[-1] = ''

        cipher_columns[-3] += cipher_columns[-2][0]
        cipher_columns[-2] = cipher_columns[-2][1:]


        # count = 0
        # if len(cipher_columns[-1]) != len(cipher_columns):
        #     diffrence = len(cipher_columns[-2]) - len(cipher_columns[-1])
        #     # Old way, resulted in adding null characters to the last 4 lists in the list not the last 4 lists equal to where they should be with they key
        #     while diffrence > 0:
        #         if diffrence == 1:
        #             i = 1
        #             print(key)
        #             print([len(x) for x in cipher_columns])
        #             while i < null_count:
        #                 # cipher_columns[-i] = cipher_columns[-i] + '.'
        #                 i += 1
        #             diffrence -= 1
        #         else:
        #             for each_car_key in reversed([x for x in key]):
        #                 # move the last character of the list to the first character of the next list
        #                 cipher_columns[-(diffrence-1)] = cipher_columns[-diffrence][-(1+count):] + cipher_columns[-(diffrence-1)]
        #                 #delete the last character of the list
        #                 cipher_columns[-diffrence] = cipher_columns[-diffrence][:-(1+count)]
        #
        #                 count += 1
        #                 diffrence -= 1

        k = len(key)
        j = 0
        for each_key_char in key:
            i = j                                                                   # reset to approroite starting point
            n = int(each_key_char) - 1                                              # Find the correct column
            for each_char in cipher_columns[n]:
                try:
                    running_answer[i] = each_char
                except:
                    pass
                print((''.join('.' if x is None else str(x) for x in running_answer)))

                i += k                                                               # Step the key size to find the next characters position
            j += 1                                                                   # Step when moving to the next column
        answer = (''.join('.' if x is None else str(x) for x in running_answer))
        print(answer)

        print(cipher_columns)
        print(key)
        self.ze_analyse(answer, key)


    def ze_runner(self, key):
        '''
        Old code, not used
        :param key:
        :return:
        '''
        # Reset the plain text output
        running_answer = ''

        # Grab each block of the cipher text
        for each_block in self.cipher_blocks:

            # Grab each position that the key defines
            for each in key:

                # unencrypt that character and add it to the plain text
                running_answer += each_block[each]

        # Run out anaylses suite on it and return a score
        # print('[+] Running analyses')
        ze_analyse = (Analyse(running_answer))
        ze_analyse.run()

        # If the score is high enough print it as a possible answer
        if 0.35 <= (ze_analyse.result/len(cipher_text)):
            print(ze_analyse.result)
            print(running_answer)
            print('+'*10)
            time.sleep(60)
            with open('results.txt', 'a') as results_file:
                results_file.write("%s, %s\n" % (str(running_answer), str(ze_analyse.result)))

    def create_possible_answers(self):
        '''
        Create a generator of possible codes and pass them to be processed
        '''
        # Make a set of the diffrent possible keys
        arrangments = itertools.permutations(range(1,self.key_size+1,1))
        print('[+] Finished generating possible keys')

        # Uses wayyyyy too much memory
        if single_thread is False:
            m = multiprocessing.Manager()
            ze_pool = multiprocessing.Pool(4)
            ze_pool.imap(self.ze_columnar, arrangments, chunksize=50)
            ze_pool.close()
            ze_pool.join()

        elif single_thread is True:
            # grab one possible key
            # for each_arrangment in arrangments:
            #     print(each_arrangment)
            #     self.ze_columnar(each_arrangment)
            self.ze_columnar([3,4,2,1])


test_text = '''
OOANWODKANRIRGLPHPEDHTTODIELELUFETSSRELHNHEIUNUCNSNSLESOTOGEMOEOOSFEBSNELT
EEDLAAGENEXCMTIRNDEOTEIWSIRTUNEENNSAAFTOHRLDNWESQEASNRTDHOIETMGSRAPFETGETSE
PISYGAOLEMOTTDROEOLHSOASEEEETCHTEOKAIFENGTVERELHYFOHESWIBTIEPVNWHYCIMRTHSNEH
IOPSOEETOHGNARAYHRAABNOBAOJOYWEEARIIATSRTMTOISLEUIOIEDAICHERCOIOGEUTERILRHGPM
ATSHPHMTEDGMHAALETMVETILRRYGKARHTYBEEDYLIBSYLTTTTUSIGMNDOLNNIWSLTORIEMEOSHEED
OEAREDOAIIRHAWEAOYYMWTOTSNISERWNWSMEDITOSIAIDESNILTIETPFELTTMFKIIDVHESCVORSERI
WISESIDSODKWLTENPEAODGTSCMIH

CIHLNGIICEVOHIFEFSOTISLTTHHSEIGNWSTYEEIAWNFAGEALONHTCUHDNDWYSEOEESTOLDHTPHSEETSV
CTEDMCCPIRBOANMTNHTAOYTTNTFWRIMHSDTLEDAGOEENEEWANOF
ENRLSMOSYMRAOEYEPSIHNWTBRNTGUOIIOSOILNTNCMNAEALTYHFAJHTAWOLNYOLYYTHSMYNLHNELCCNJ
YLOMAELAHANOTTELARNEIIMNHREPISAWRRGNRTNDRTUNMRSTMHOCUIEPEROUSGAAOHCIFATHLGHETEEE
DEEILPTEHLTASORAWLEWNWOAIITWAYVNOMETONSTOWEAESLIHRFESSOATLAETNQBREGFASKTEHDTHUTIE
UTAAPIAERCANISXEANSEUEWTASGALFTNRTTSELMTIGSTETDAPRHLEPRUWTCLSEHLEDTAMNILOBEOSECEI
AETTESIBOAPNBELASIOOEETHCELETKOT

FNYOGNAWNINSHHDESDOSNDTIBSBDENSNIAFYAOOMTTINEDNEV
OITOOEDAWOCTNDTIYSEIEMETFORESPISVWIYIOEEULUOTIYGEMNDSILVAIARANLSEEATANOEOLTONAETW
TSFENIBIAHBHALRSOPSORHOASLIATRWIOYOESTOIIGTUNHUSICUHISLHVTEDAEWNNACRNIPPANNGMPEO
REBATRMERTNACGEOETAPOLTTTORSVHDMTFWAMALITEOEONEROIARMWPHNTTTSRPSMMKSIUMAHOTTCFST
OSHLPLRIHALSEGISEOEMNAPIONYTHTSEPOOTETGTRTTSTOTESUTOMEYTYREOJOHHILKTICNWGOSSRIE
EIBRANRISUDEHECEUKFSTTOTNLACOFLORBMTBWNTSTEIWRRCAQOWELMOPLTRWVMQESUSNEOAHVCCOIL
PNHDOOOSKUURTSYWLPRTOLAMAEOLWCIIWMIWVOYUUIQERVNAICDOSITEPOKOPEEMEYIUEIRTPRFIEUE
OEODINKSEHYFENICROGEHITNNTHDTTAFSELNBVYCTSHTAHHERIAEAMECDTTOTSVILOOIDRSOISTULHS
TGTVOTTGBOYCRVCNKSIEFRBWOLTDIFTGTYRLISSHEEDEIIOIDSTERLTTYTHWLKVETMUYTHWNRYRTUK
AASNPTDUTNOTNNHNAACICIDYITHYGEAULNAWOCSLTMVRRPTEAHPNTIABIKFOIIHTAEGOUETHOOKHPSO
TSWLSNEEWLREHOMTWERTNRPHSTPIOULETCDIOAALNRSCIHSREHAOHIGMBELITBIINLSMFLATVALOREA
VARELEKALOISENIIGMALPNSAROENDHTESTBNASETGERTSIREITXOIBNUTWETYEIOACLKRYRDAEEEMG
OHALSIODEALORABSNIIINBNSYLTALEAYRRSDNSIDSWEABNURIR

TNCCNTUIWKEOPIHSNILDLHAFCVOMLRRATRTAOIEELIROENSNOVEETTELAIEAS
NOLTHBRHSLETEYOAMMLTTNTSEGTHHOSAAMLNMRRWARAILT
ONAEEAEALFEPHPETFYTKITLCFESCYEIOPSITEHOCOIOIENEUIQEWAEUOTFEETCYFAWSYINCTYSDTWO
TOGEVSISCARRDAITCCEDHULFRNOPEOOTRAUNLHGTOEDGCSEEETSREFRHTTOOSESSWELMDNASEEMIFB
EIAKRDSPNRRHOAHHSWMNOAGECEEIHIEPCMORCANETFNEEUIIWAMIYOIENDETXEOUCAULEEGRUTTODN
RLGREBDOPHALTTLSVLHBERYNTTOYVAHAMCBSCHEATAGSRCCNULBNEWOAOEYTWEPIEBRIONNNULAHAIO
HHEEEGTEIAIAFAAHECANOTPEWOFETONOEMSNYTINITTESDSWYRRAEECGMORBCNMNNLSKNADBTHWYEH
IATDKTDYETHNIFNEHMISFAIRAESDHGAOMEREOUYTMTCPIEDMIEMENRTVATHDWNOBUTFALOODHRLIOEH
IEEMIOHEEIAMNHAEUIMIMOSPODPEHUAETDNOTHNUSNANCIYORAANDWKEHATEHDMSHFIMARAWPEIAOA
AIFKEUIOOSAEOOETFIUCTRHSETBMAELGHUAHNWIUHRYAMPARIRGTTAMDNRNCEISOFSIAHSMIORHOME
OAELSDGTGTLNUMCOYIHAUEDKFLEEWAODUOIRTNLGOOISSSAAATGSETFAAOYOSARORPELAIITOENGLOI
SANOGAEEMSSSOENNTTSETDAITYTGTEELAPLNAWSUPTHLBMOORRLVSLUORCSRNAQOGEMOIASHSETUTI
DOHTHOTDPIAVOSVOITUOTWCMHRTNWOCIITTOUAYAFNRLWUIAAHTTNEIDIREOMOFANETSETCBEHNTHO
PNNGESSREHLGTLEEITMEHGLLRHNETCCOILRLEDIIECATLYTDEEASEMEONEMPRWUSWVKIDWHFOEETKEA
UNLDKFUORTOOOSLTVIRLOAOOCDSIANTOAERDOOTEGDECEEEBNDTLNVTOLIMEFENTLIIAEMNHKWOONAR
HHEOTMMOSCVAHMEUTWSOTUIHDDFUTOTITUPSTSTIOHPCYEPTNATTMODHRONTHHFYAFDTVTAEKTWYNUN
TTLENTIOKOEASIUYIINLYFHWTFDHALCWLTHTDALWNOTEMOYEETRENTISDDAUGNLUNDBHALDTHTOVHOIF
ESHRRHSHHALORLEEHNYHEUTEHUATENPMOHRWRGALNDSOAAPEDWIWLMEOEYAKFLEKHRAAOOMUUEEEAEO
NONHFLHTIAWAAONYNNALIEEFDUUNRTAUHAHONTWYOTOHNESRASRPNUIRASTAMTAAHESTTSTSETEAYKR
NTGSHICHDTOE
        '''
test_text2 = '''
        SOMMDIDGAATIIYHIHSNDEN
'''
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


for each_keysize in range(1, 8, 1):
    print('[Running key size] %s' % str(each_keysize))
    trans = Trans(test_text2, each_keysize)
    trans.create_possible_answers()
