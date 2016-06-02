import functools
import multiprocessing
import itertools
from math import ceil


single_thread = False
# known_word = 'COMP3441{'
class Trans:
    def __init__(self, cipher_text, key_size):

        self.cipher_text = cipher_text

        self.key_size = key_size

    def factors(self):
        '''
        Gets the factors of the length of the cipher text
        :return: List of integers that are common factors of the length of cipher text
        '''

        n = len(self.cipher_text)
        return list(set(functools.reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))))

    def ze_analyse(self, answer, key):
        '''
        Analyses the calculated answer to determine if it indeed english
        :param answer:
        :param key:
        :return:
        '''

        if known_word:
            if known_word in answer:
                print(answer)
                with open('results.txt', 'a') as results_file:
                    results_file.write("%s | %s\n" % (str(answer), str(key)))
        else:
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
                cipher_columns[int(each_key_char)-1] = cipher_columns[int(each_key_char)-1][:-1] + '.' + cipher_columns[int(each_key_char)-1][-1:]
                null_count -= 1

        new_column_size = ceil((len(self.cipher_text))/(len(key)))
        self.cipher_text = ''.join(cipher_columns)
        cipher_columns = [self.cipher_text[i:i+new_column_size] for i in range(0, len(self.cipher_text), new_column_size)]

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

                i += k                                                               # Step the key size to find the next characters position
            j += 1                                                                   # Step when moving to the next column
        answer = (''.join('.' if x is None else str(x) for x in running_answer))
        self.ze_analyse(answer, key)


    def ze_runner(self, key):
        '''
        Decrypts by creating blocks and decrypting each block with the key
        :param key:
        :return:
        '''

        cipher_blocks = [self.cipher_text[i:i+self.key_size] for i in range(0, len(self.cipher_text), self.key_size)]

        # Reset the plain text output
        running_answer = ''

        # Grab each block of the cipher text
        for each_block in cipher_blocks:
            # Grab each position that the key defines
            for each in key:
                # unencrypt that character and add it to the plain text
                running_answer += each_block[each-1]

        self.ze_analyse(running_answer, key)

    def create_possible_answers(self):
        '''
        Create a generator of possible codes and pass them to be processed
        '''
        # Make a set of the diffrent possible keys
        arrangments = itertools.permutations(range(1,self.key_size+1,1))
        print('[+] Finished generating possible keys')

        if single_thread is False:
            m = multiprocessing.Manager()
            ze_pool = multiprocessing.Pool(4)
            # ze_pool.imap(self.ze_columnar, arrangments, chunksize=50)
            ze_pool.imap(self.ze_runner, arrangments, chunksize=50)
            ze_pool.close()
            ze_pool.join()

        elif single_thread is True:
            # grab one possible key
            # for each_arrangment in arrangments:
            #     print(each_arrangment)
            #     self.ze_columnar(each_arrangment)
            # # self.ze_columnar([3, 4, 7, 1, 2, 6, 5])
            self.ze_runner([8, 2, 6, 1, 3, 4, 7, 9, 10, 5])
            #8,2,6,1,3,4,7, 9
            #YOUCOULD

if __name__ == '__main__':
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
            ORISDFETSCIOEPRLNTNOTNISAYRODTWWETCUSFTSNIENOPICUCHCUARSSIBLIKWDOEHAEAHOMSAHIOFRTAEFRTIEOMRAPIOUDNEOTRREYRDELN
    '''

    test_text3 = '''
    CNASNLRGLETWTEGITFOSSLOIRCREOSANCNDRPENALNIWOSSTIOOANIIVITAXISHATPEFLISERSOIWTUTDEOIEELPTSESTILLLHDWMROOOWNPTUODRNCROCN
    TPFTEEERRIEWHMROMHITPASNCNKERLUTPIVSIENORNNIEETNMIMTIHTHEEEROCUOFATAXMROOHMOKGELRSTNETHITNAEDHHXIUNISMTUPHHTODALNRXELEI
    TPITUOIEB
    '''

    test_text4 = '''
    HIIFA STMPT TITET SSNCU OSFCE LUSRO WEOPP NASEL LACEI ANONF OTHLL ENGOW ABIWI SIHTS ICMET OXWEH AHSTM AALEK LTOWA EGRRA THDNE ETTOE HGKER MEPAW EACHS EGIAL EVLER GELAN ANFII CNUPA LOPSN DRTTI ANDIS REUOD STHTO EXATC IMTOO IERSQ UCORE NLOTH TSERI TEOTR NNRYW EIICM ETOXS AEXDN AZOAR ANIDE THATE ARILL ESTOE FOYTR SUFTE OMETL TNE
    '''

    son_of_rail_fence = '''
    S_   ltes e__owesft4ya'h r_ernadinhohn_hstfeamion coo iost  lhrooidskeutsio t,aPeeut_eemlc tmkhegi_wschoool31neOen Cbale4h s tee_  oi_r yjnsr  iat_.>dslu}4 nd asthsnCg\  it_ Misdirection_tCaeesa Oe1elr__firiOR_lelsmk_hlabsfkabM{fbbliuec_p  eiecn P1oaubco a_ite_headm34rebihchtHo4c
    '''


    for each_keysize in range(1, 50, 1):
        print('[Running key size] %s' % str(each_keysize))
        trans = Trans(son_of_rail_fence, each_keysize)
        trans.create_possible_answers()
