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


single_thread = False
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
        n = len(self.cipher_text)
        return(list(set(functools.reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))))

    def ze_analyse(self, answer, key):
        # ze_analyse = (Analyse(answer))
        # ze_analyse.run()
        word_list = []

        for each_word in open('sowpods.txt', 'r').readlines():
            if len(each_word) > 4:
                each_word = each_word.replace('\n', '')
                if each_word.upper() in answer.upper():
                    word_list.append(each_word)

        words = ''.join(word_list)
        print('*'*10)
        print(len(words)/len(answer))
        print('*'*10)
        if (len(words)/len(answer)) > 0.3:
            print(len(answer))
            print(len(word_list))
            print(answer, key)
    def ze_worker(self, inq, outq):
        self.ze_columnar(inq)
    def ze_columnar(self, key):
        # print(key)
        # if len(self.cipher_text)/len(key) == int(len(self.cipher_text)/len(key)):
        #     pass
        running_answer = [None] * len(self.cipher_text)
        key = ''.join([str(x) for x in key])
        column_size = int((len(self.cipher_text))/(len(key)))
        cipher_columns = [self.cipher_text[i:i+column_size] for i in range(0, len(self.cipher_text), column_size)]


        k = len(key)
        j = 0
        for each_key_char in key:
            i = j                                                                   # reset to approroite starting point
            n = int(each_key_char)-1                                                # Find the correct column
            for each_char in cipher_columns[n]:
                running_answer[i] = each_char
                i += k                                                               # Step the key size to find the next characters position
            j += 1                                                                   # Step when moving to the next column
        answer = (''.join('.' if x is None else str(x) for x in running_answer))

        self.ze_analyse(answer, key)


    def ze_runner(self, key):
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
            for each_arrangment in arrangments:
                # print(each_arrangment)
                self.ze_columnar(each_arrangment)


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

for each_keysize in range(1, 50, 1):
    print('[Running key size] %s' % str(each_keysize))
    trans = Trans(cipher_text, each_keysize)
    trans.create_possible_answers()
