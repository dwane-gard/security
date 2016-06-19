# from co_incidence_index import CheckIC

import co_incidence_index
import kasiski
import multiprocessing
import itertools
import time
from functools import reduce
from word_search import WordSearch
lock = multiprocessing.Lock()
# 0 = Brute 1 = dictionary

class Answers:
    def __init__(self, ze_ic, ze_key, plain_text, E, A, T):
        self.ic = ze_ic
        self.key = ze_key
        self.plain_text = plain_text
        self.E = E
        self.A = A
        self.T = T

class decode():
    def __init__(self, cipher_text, approch):
        self.core_count = multiprocessing.cpu_count()
        self.common_words = open('commonwords.txt', 'r').readlines()
        self.approch = approch
        self.debug_flag = 0
        self.analyse_code = False
        self.cipher_text = cipher_text
        self.cipher_text = self.cipher_text.replace(" ", '')
        self.cipher_text = self.cipher_text.replace("\n", '')
        self.cipher_text = self.cipher_text.replace(".", '')
        self.cipher_text = self.cipher_text.replace(",", '')
        self.cipher_text = self.cipher_text.replace("'", '')
        self.cipher_text = self.cipher_text.replace('"', '')
        self.cipher_text = self.cipher_text.replace('?', '')

        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z']
        self.count = 0
        self.possible_answers = []

        f = open('sowpods.txt', 'r').readlines()
        self.all_keys = [x.upper().replace('\n', '').replace(' ', '') for x in f]
        # self.possible_sizes = kasiski.Kasiski(self.cipher_text).multiples_list
        # self.possible_sizes.sort()
        self.possible_sizes = [x for x in range(1, len(self.cipher_text))]

        self.possible_sizes = [1]
        # print(self.possible_sizes)

    def start(self):
        multithread = True
        # Brute force approch
        if self.approch == 0:
            if multithread == True:
                for each_key_size in self.possible_sizes:
                    print('Brute Forcing %s' % str(each_key_size))
                    # key_set = self.product_with_prunning(''.join(self.alphabet), repeat=each_key_size)
                    key_set = itertools.product(''.join(self.alphabet), repeat=each_key_size)
                    m = multiprocessing.Manager()
                    ze_pool = multiprocessing.Pool(self.core_count)
                    # ze_pool.imap(self.run, key_set, chunksize=100)
                    ze_pool.imap(self.decrypt, key_set, chunksize=100)
                    ze_pool.close()
                    ze_pool.join()
            elif multithread == False:
                for each_key_size in self.possible_sizes:
                    # key_set = self.product_with_prunning(''.join(self.alphabet), repeat=each_key_size)
                    key_set = itertools.product(''.join(self.alphabet), repeat=each_key_size)
                    for each_key in key_set:
                        self.run(each_key)

        # Dictionary approch
        elif self.approch == 1:
            keys_to_try = []
            for key in self.all_keys:
                if len(key) in self.possible_sizes:
                    keys_to_try.append(key)
            m = multiprocessing.Manager()

            ze_pool = multiprocessing.Pool(self.core_count)
            ze_pool.imap(self.run, keys_to_try)
            ze_pool.close()
            ze_pool.join()
        else:
            keys_to_try = []
            exit()

    def analyse(self, deciphered_message, key):
        start_analysis = time.time()
        word_list = []
        words_len = 0

        # Check IC
        checkIC = co_incidence_index.CheckIC(deciphered_message)
        checkIC.run()
        ic = checkIC.ic
        if self.debug_flag == True:
            lock.acquire()
            print(deciphered_message)
            print(ic)
            lock.release()
        checkIC.run_with_counter()
        E = checkIC.E
        A = checkIC.A
        T = checkIC.T
        X = checkIC.X
        J = checkIC.J
        Z = checkIC.Z
        check_by_ic_first = True
        check_for_words = False
        check_for_letter_frequency = True

        if check_by_ic_first is True:
            # print(ic)
            if ic > 0.06:
                if check_for_words is False:

                    lock.acquire()
                    print('+'*20)
                    print(deciphered_message)
                    print(E, A, T)
                    print(Z, J, X)
                    print(key)
                    print(ic)
                    lock.release()
                    open('results_brute_force_vigenere.txt', 'a').write('%s | %s | %s \n' % (str(words_len), deciphered_message, key))


                else:
                    word_search = WordSearch(deciphered_message)
                    word_search.run()
                    words_len = word_search.words_len

                    if words_len > 0.9:
                        print(words_len, len(self.cipher_text))
                        lock.acquire()
                        print('+'*20)
                        print(word_list)
                        print(deciphered_message)
                        print(E, A, T)
                        print(Z, J, X)
                        print(key)
                        print(ic)
                        lock.release()
                        open('results_brute_force_vigenere.txt', 'a').write('%s | %s | %s\n' % (str(words_len), deciphered_message, key))


        else:
            word_search = WordSearch(deciphered_message)
            word_search.run()
            words_len = word_search.words_len

            if words_len > 0.7:
                print(words_len, len(self.cipher_text))
                lock.acquire()
                print('+'*20)
                print(word_list)
                print(deciphered_message)
                print(E, A, T)
                print(Z, J, X)
                print(key)
                print(ic)
                lock.release()
                open('results_brute_force_vigenere', 'a').write('%s | %s | %s\n' % (str(words_len), deciphered_message, key))
        print('analysis time: %s' % str(time.time() - start_analysis))

    def beaufort_decrypt(self, key):
        pairs = zip(self.cipher_text, itertools.cycle(key))
        result = ''
        for pair in pairs:
            total = reduce(lambda x, y: self.alphabet.index(y) - self.alphabet.index(x), pair)
            result += self.alphabet[total % 26]
        if self.analyse_code is True:
            self.analyse(result, key)

        return result

    def decrypt(self, key):
        # rewritten decyption module
        # time is very similar to run
        start = time.time()
        pairs = zip(self.cipher_text, itertools.cycle(key))
        result = ''
        for pair in pairs:
            total = reduce(lambda x, y: self.alphabet.index(x) - self.alphabet.index(y), pair)
            result += self.alphabet[total % 26]
        print('decryption time: %s' % str(time.time() - start))
        self.analyse(result, key)

    def run(self, key):
        # decryption module
        # start = time.time()
        # if self.prune_keys(key) is False:
        key = [x for x in key]
        key_size = len(key)
        cipher_list_sized = [self.cipher_text[i:i+key_size] for i in range(0, len(self.cipher_text), key_size)]

        deciphered_message = ''
        for each_part in cipher_list_sized:
            x = 0
            for each_char in key:
                try:
                    key_letter = self.alphabet.index(each_char)
                    cypher_letter = self.alphabet.index(each_part[x])
                    deciphered_letter_index = cypher_letter - key_letter
                    deciphered_letter = self.alphabet[deciphered_letter_index]
                except:
                    deciphered_letter = '.'

                if self.debug_flag == 1:
                    # pass
                    print('[cypher letter] %s | %s' % (str(self.alphabet[cypher_letter]), str(cypher_letter)))
                    print('[key letter] %s | %s' % (str(each_char.upper()), str(key_letter)))
                    # print('[shift] %s' % str(deciphered_letter))
                    print('[new letter] %s | %s' % (str(self.alphabet[deciphered_letter_index]), str(deciphered_letter_index)))
                    print('\n')

                deciphered_message += deciphered_letter
                # print(deciphered_message)
                x += 1
        # print(deciphered_message)
        # print('decryption time: %s' % str(time.time() - start))
        if self.analyse_code is True:
            self.analyse(deciphered_message, key)

        return deciphered_message
        # else:
        #     pass


    def prune_keys(self, key):
        multiples_list = kasiski.Kasiski(''.join(key)).multiples_list
        multiples_list.remove(len(key))
        key = ''.join(key)
        len_key = len(key)

        for each_completed_keysize in multiples_list:
            x = [key[i:i+each_completed_keysize] for i in range(0, len_key, each_completed_keysize)]
            # print(x)
            if self.check_if_all_equal(x) is True:
                    # print(each_completed_keysize)
                    # print('Prunning: %s' % str(key))
                    return True
            # else:
                # print('not prunning: %s:%s' % (str(key), str(x)))
        return False

    def check_if_all_equal(self, iterator):
        try:
            iterator = iter(iterator)
            first = next(iterator)
            return all(first == rest for rest in iterator)
        except StopIteration:
            return True

    def product_with_prunning(self, *args, repeat):
        # C version ttp://svn.python.org/view/python/tags/r271/Modules/itertoolsmodule.c?view=markup
        # This has to compute before generating using lots of memory

        # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
        # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
        pools = [tuple(pool) for pool in args] * repeat
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        for prod in result:
            output = tuple(prod)

            if self.prune_keys(output) is False:
                yield output
            else:
                pass


if __name__ == '__main__':
    # test = decode('TIKSJUGPKNHVOCGAWGRZGVFPTGWLFXEOKNH', 0)
    test = decode('IXCSX QRLKN HCTBU TBTTV RTFNC PYHPY ATIEU VIOII OVOFV HFTNF VTBKL TCNEK XXGPV VERWI QOEOV IOCLP VOGTD QCRUA DBVAD GNUTE TCSUJ EZYES GTIGB FUTQN ADGTP EOOPE DVWJV HJUPT CNEQT IGRDC RSKES UTIKS QCRUK CVNAS FAUCC FPTSG WBUOO GOGVH FQLEG RPPET JAEDE FPFVN LGQRZ GASUA OFTIG CPOPB PYUJA UQPFT AUGDJ VHBFL PPGTK NDGFP EUTGD UJEJT AUVEO VIPPO OVHFK ROGWF TSIKN JGREC TBEEO VRFVH BVIUY ATCCU WAMNY QQSTK BMGTP UTJNL CWYTR ADGIO QNFIU ZYHPK LMEAM NDJEK XCSSG SQQNT KBMGF PTBPV HBPDE KDOVG JXEBE RBRAC QUUVH FQLEQ NFUIO EEUJE SGWBU NPUTS WCUWR FFCBD LJPGB PDJVW BUINR OTUIC NEUQG FVAOA OOGOV VTPKN TVAMN AOAPF QPMGJ VUTSC NUJEJ TOXPC BDLJP GVPDF TTIGF MQOSC NEVHF TEXGR FPOSG CPTDT CSUQW IGRFC NZQFJ VWFPT JFVJU IUGDU JESQO NVOJP SUCLM CSXKT DJWIG NJPOU KCFFT ICTUJ EBKRD QNEKT JQNFT WIKCI YATTI HJTOG XUVOP WRSCC LJAEV WPTEE NIHJT TQNJV SEKSQ NAZRA OGLNK NPTAM CRNZM BLOSC LBTMY EOOEE SPEEK PJEKF FUQVH FRHPP EDJHP RSLAH FADJE KJVHJ PKUJE SGSBR RPDLF OWJVH UJEBE DPYNI GRFKT TIOUC CPWPM GOGRR FVTZU ESKOV ULPQK JPGBN ASOLJ IHUUO OKTBP DUJES QONKS BNIUV LFYAS OESVH BPNPT MBNYP WSIQU MFPSQ BBDLZ EHFEK JVOVV DJEKP JOLCY UJAOM SGQRM GTUKN HOELP OXKLM NOPMI OVOJV TIKSX CSIKS VUUBN RFUPP PSFYH JEHXC SGQLM QWFFU QDYIK SVUUB NFPNL PYUQY HJEHX CSUQD PCBTQ LVVEM ANPVH JPGUY OXGEL ULBVE SKWFP TCCCL VOEQS POEQC TDJIO IAOFN PVIDG DUJEM KGIVS XGRFU TJNLP PCIJO QUKZJ EZVHF UEBNA SOLJI HUUAS GOOCG BKNKW SUVHP WGIVY PWSIQ UMFKO QWXJA UGVFT YPWFJ ZEEOU TVNUJ AWGTB MEOFI DMOIQ KBATI CNLUF PTLFV TJPGN GKOQW JNLMQ OLKNU QIUKS JIHFF AOFWB NKFFB BEKUQ TIGOG HIDGA CQUUC MPPTI NAUGR JYATU IUVIO IAUOY EGSLE ATWAM NYQGR VUIOI TIGGS CPIKN HUYTV ENYHF PIOQT JEEEV HBVPF GRJPG UTAGH IDYAT FRPRP JPGPH FOQTT NOXNY CWTPP ECKGD JUOMA UCTJO EHGTU KNHNO XGRBP DMQWF TEWGR ZHEXO IOWTF UISCC FFTPH IOFOV VWIGT IGRXG HBFAH TAQJI OIPSQ BMGMC WTRWI DMLZP OUKCF FTICT GQRFX ESADS QPPHF JPTSC FGKCU JESQU UGRXC SSGPP TTJPG PPEMG STREF TPFGR TYESG DSQPQ KNHQF GVHFP EUYOS MBVVH PYIPU BVIMF OOSAL FCKUJ EOKTI KTNGA MNOGV HFREF TSETO QRIOI OGHWF TEJPT ICTEE AOFTI GYXGR FFRPR PJPGP HFJPO SFESQ FQTOY KMJVY UQOVT RBEKJ EAMNE EFIDM BVVHJ UPIQN FFIEP TFXEO TIOIA OFIUF IEPTH QTPXO JEENC IMLUT VFBKL FFISC NPWTP HTIGO GHIDG AOFSQ TIOVE EQFGF OXPTI GSUTE FVTPV HFFCV ROODU TVIOI TITOV IHUJE EQOSK HFCRE CVFTY XGISF SPWNE WPPPT BMIOI MZHIS UTTVE QKTXC SNQSU FEGKN JVEMA ATRLB UHJNO PMEEF OXPAO FIXCS TVAOF IOIIO CNJPC IQFXC TFTAC QVFCR BKSFF FMQOS EMEGE QHIMN EEYIU JCBDL FUDJT EDVLZ PEYVT PVHFD AUVES ABBPK PHTIG UQUWI KCIYA TQPFP WJVHF ZPPUE EYISK NHJEB TTKWM QGDJP TPOYN QUUJP PWNEK NHNIL GAKCC LJANO ESKMB DOVVT PFIFD UUKDJ FNUCN EKVFT YTNOX NYBPD DCRFH UMNYU QOLCS UGPCC CLQNU QDSAG SQUOF LPQKJ PGVRT PVHFG NEQFU JESQW JUAXV WPVRB FETOE OYIUJ SPOEG NOPTT JNETW PBRUN RAOFA MCRHG DSAES EHIQP TMYXJ AUVHF JEMNH BRPFP EEYHF TEJUD JEKBP DXJYJ UNUJI TRHPP EXQRL KNHVR BFIFQ HBDOV VTITE FAEBT SBIOE WRJPG UJEZG ASNYT GRWKC FKNPV IDGDU JAUVH FRLVI CBROO VHFJI HJPSG STWRF EHJNL FFWBV ESNOP RHBFD FXEMQ PFFAD TADMA OFWBU FBKLJ PGJVO MFDJE KBDOV VIUCT UJEUK MFCNE JETCI EJEEN OPMIO VOJVI HWETU HFFIE PTCGC BWSFK TXCST VIMNL JMEUJ ITVHF NATVT XQYFC RTYED CMFKN UQSFT VJEEJ VTIKS NQROK NHCNE KTBRP FFIUV OTGEJ HIUYA TQNUK GIVLZ NOOIS UQRZU HPTTJ VLJVE SCLMA EYRLP FEEPO XVHJU BVKLE KNHYA TCBPW TTVOS KETJI HJAOF WFYES GOONE WGLUJ EDJIM NESUF PTTIG AJTCP PDJVI PPESU WFTEP PTIGR PQFTQ BZVHF VINGT IGWBV ESKSP PLFXE MKTTT EBNLZ JIHJP SGSTW RFYHF PTIGC BRRVR TVTEE YAUGR DCMFQ UUUOI CRECN EHATV TICTJ VSIQT UJEDQ NDTEU GFMQO SVIMG WFKGI KNHMG BVLFC SUWPP HFUJE GNOPT AOFKJ EKFFI UWPUQ AEGGS GEBPG MGTVT NJPGU JETKN HNECN ATVOG YAUGR JPTPC HJIHQ TETUU SGSQT IOMLF TWIKC INICG RBNLZ FOVUE EVHFH ISUTU JRFGR BEKTY IUJWB VESVH FHISU TUJRF GRBEK TEOOV AJPEE VHFRR JOASA AOFBB EKVRC PTEWQ IDGSX KTDJE THOSV HFEON RAOAF PTTIG EOVIS GSUCT FAEQK CPWLE PTDCL MFIDM BFEAV UEBNL NQBJN ETGRW KCFUA OFMPU TGKXF FLJPE TGRWK CFUFP TTICT DCRSK ESYES GDPYN UJETW BGNOP TSMQW MAFJN LFFUQ YIUJW BVESV ALKNH QUUTA DMSPP ECAOO GATKT IKTUJ EJTPP YESEO OPEDV IPPSB NLUJE DQPQG RDCBM KNHWN EGRUJ EGNOP TWBUR VKNFF HVPDS GDTKF OQTUJ OVUAO FSPHI OVEST ADMPB VCIGS BNLEG AEVHB PKGWL MAIUJ AEUTP RPFFC NUHZQ FTRIM NIOIO WGRJP TPVHF WPTDA UVESA BBPKX JIDJW PWLEJ AWGKJ NLFFM FKNTV AOVLZ DYTJE FTLVE KQTEQ CRBVI PPOVT RBEKX CSTCF FYEXG RFVHF OOTVU QJIMN OOVHF UUCHL PQRBP DJJAE OAEGS VTEUJ AUYHF POVTP PYESY ATKNT VAMNE EVHBV IHQTB CSDTE XKNXC TFTPS QOGEO OPEDV OSCNE CLUJO VIHJV WBUWF VWFYE SGVFT YNWCI UTJNL PRESC TJPGB PDTVI MNOON IOGTI GDDKS OQLPP GFTOQ GRBVI OIATC RERAS VYSQO NCNEN IUGRB NLZGV FTYDW SUQMF THBUM PXEEQ UUPEY VTJOE JEAMN EEKNT QMFQN FGLTG AOUWF TEEFI DMSQJ OOGAO FIOVR PFUDG DIKMT GLGCS UJEOG WGCCJ NIUAM BPAHG RJVOM FHJOI OGEEG DUQGF VSPOE GKBSG PBVCI KNHKN TVAMN EEVOB POUJE SHLPQ RPHTI GBVKL EKNHC NEVHB VIEUT BTTFF TIGPS QCFUS XKTIF IDMBV VDJFN UIEUC RFUPP PSFVO NALBU TFOAJ NNFYD JEKPJ OLCYU JAOMS GQRMG TUKNH OELPO XKLMN OPMIO VOJV', 0)
    test.start()





#
#
#
#
