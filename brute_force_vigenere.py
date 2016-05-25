# from co_incidence_index import CheckIC

import co_incidence_index
import kasiski
import multiprocessing
import itertools

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
        self.common_words = open('commonwords.txt', 'r').readlines()
        self.approch = approch
        self.debug_flag = 0
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
        self.possible_sizes = [3,]
        print(self.possible_sizes)

    def start(self):
        # Brute force approch
        if self.approch == 0:
            for each_key_size in self.possible_sizes:
                print('Brute Forcing %s' % str(each_key_size))
                key_set = self.new_create_brute(each_key_size)
                m = multiprocessing.Manager()
                ze_pool = multiprocessing.Pool(4)
                ze_pool.imap(self.worker, key_set)
                ze_pool.close()
                ze_pool.join()

        # Dictionary approch
        elif self.approch == 1:
            keys_to_try = []
            for key in self.all_keys:
                if len(key) in self.possible_sizes:
                    keys_to_try.append(key)
            m = multiprocessing.Manager()

            ze_pool = multiprocessing.Pool(4)
            ze_pool.imap(self.worker, keys_to_try)
            ze_pool.close()
            ze_pool.join()
        else:
            keys_to_try = []
            exit()

    def analyse(self, deciphered_message, key):
        word_list = []
        words_len = 0

        # Check IC
        checkIC = co_incidence_index.CheckIC(deciphered_message)
        checkIC.run()
        ic = checkIC.ic
        E = checkIC.E
        A = checkIC.A
        T = checkIC.T
        X = checkIC.X
        J = checkIC.J
        Z = checkIC.Z
        check_by_ic_first = True
        check_for_words = False

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
                    open('results_brute_force_vigenere', 'a').write('%s | %s | %s ' % (str(words_len), deciphered_message, key))
                else:
                    for each_key in self.all_keys:
                        if len(each_key) == 2:
                            continue
                        if len(each_key) == 3:
                            continue
                        else:
                            if each_key in deciphered_message:
                                word_list.append(each_key)

                    words = ''.join(word_list)
                    words_len = (len(words)/len(deciphered_message))
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
                        open('results_brute_force_vigenere', 'a').write('%s | %s | %s ' % (str(words_len), deciphered_message, key))


        else:
            for each_key in self.all_keys:
                if len(each_key) == 2:
                    continue
                if len(each_key) == 3:
                    continue
                else:
                    if each_key in deciphered_message:
                        word_list.append(each_key)


            words = ''.join(word_list)
            words_len = (len(words)/len(deciphered_message))
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
                open('results_brute_force_vigenere', 'a').write('%s | %s | %s ' % (str(words_len), deciphered_message, key))

    def run(self, key):
        key = [x for x in key]
        key_size = len(key)
        cipher_list_sized = [self.cipher_text[i:i+key_size] for i in range(0, len(self.cipher_text), key_size)]

        deciphered_message = ''
        for each_part in cipher_list_sized:
            x = 0
            for each_char in key:
                key_letter = self.alphabet.index(each_char)
                cypher_letter = self.alphabet.index(each_part[x])

                deciphered_letter_index = cypher_letter - key_letter

                if self.debug_flag == 1:
                    print('[cypher letter] %s | %s' % (str(self.alphabet[cypher_letter]), str(cypher_letter)))
                    print('[key letter] %s | %s' % (str(each_char.upper()), str(key_letter)))
                    # print('[shift] %s' % str(deciphered_letter))
                    print('[new letter] %s | %s' % (str(self.alphabet[deciphered_letter_index]), str(deciphered_letter_index)))
                    print('\n')
                deciphered_letter = self.alphabet[deciphered_letter_index]
                deciphered_message += deciphered_letter
                # print(deciphered_message)

                x += 1
        #    print(deciphered_message)
        self.analyse(deciphered_message, key)


    def new_create_brute(self, key_size):
        arrangments = itertools.combinations_with_replacement(self.alphabet, key_size)
        return arrangments

    def worker(self, inq):
        self.run(inq)

if __name__ == '__main__':
    # test = decode('TIKSJUGPKNHVOCGAWGRZGVFPTGWLFXEOKNH', 0)
    test = decode('IXCSX QRLKN HCTBU TBTTV RTFNC PYHPY ATIEU VIOII OVOFV HFTNF VTBKL TCNEK XXGPV VERWI QOEOV IOCLP VOGTD QCRUA DBVAD GNUTE TCSUJ EZYES GTIGB FUTQN ADGTP EOOPE DVWJV HJUPT CNEQT IGRDC RSKES UTIKS QCRUK CVNAS FAUCC FPTSG WBUOO GOGVH FQLEG RPPET JAEDE FPFVN LGQRZ GASUA OFTIG CPOPB PYUJA UQPFT AUGDJ VHBFL PPGTK NDGFP EUTGD UJEJT AUVEO VIPPO OVHFK ROGWF TSIKN JGREC TBEEO VRFVH BVIUY ATCCU WAMNY QQSTK BMGTP UTJNL CWYTR ADGIO QNFIU ZYHPK LMEAM NDJEK XCSSG SQQNT KBMGF PTBPV HBPDE KDOVG JXEBE RBRAC QUUVH FQLEQ NFUIO EEUJE SGWBU NPUTS WCUWR FFCBD LJPGB PDJVW BUINR OTUIC NEUQG FVAOA OOGOV VTPKN TVAMN AOAPF QPMGJ VUTSC NUJEJ TOXPC BDLJP GVPDF TTIGF MQOSC NEVHF TEXGR FPOSG CPTDT CSUQW IGRFC NZQFJ VWFPT JFVJU IUGDU JESQO NVOJP SUCLM CSXKT DJWIG NJPOU KCFFT ICTUJ EBKRD QNEKT JQNFT WIKCI YATTI HJTOG XUVOP WRSCC LJAEV WPTEE NIHJT TQNJV SEKSQ NAZRA OGLNK NPTAM CRNZM BLOSC LBTMY EOOEE SPEEK PJEKF FUQVH FRHPP EDJHP RSLAH FADJE KJVHJ PKUJE SGSBR RPDLF OWJVH UJEBE DPYNI GRFKT TIOUC CPWPM GOGRR FVTZU ESKOV ULPQK JPGBN ASOLJ IHUUO OKTBP DUJES QONKS BNIUV LFYAS OESVH BPNPT MBNYP WSIQU MFPSQ BBDLZ EHFEK JVOVV DJEKP JOLCY UJAOM SGQRM GTUKN HOELP OXKLM NOPMI OVOJV TIKSX CSIKS VUUBN RFUPP PSFYH JEHXC SGQLM QWFFU QDYIK SVUUB NFPNL PYUQY HJEHX CSUQD PCBTQ LVVEM ANPVH JPGUY OXGEL ULBVE SKWFP TCCCL VOEQS POEQC TDJIO IAOFN PVIDG DUJEM KGIVS XGRFU TJNLP PCIJO QUKZJ EZVHF UEBNA SOLJI HUUAS GOOCG BKNKW SUVHP WGIVY PWSIQ UMFKO QWXJA UGVFT YPWFJ ZEEOU TVNUJ AWGTB MEOFI DMOIQ KBATI CNLUF PTLFV TJPGN GKOQW JNLMQ OLKNU QIUKS JIHFF AOFWB NKFFB BEKUQ TIGOG HIDGA CQUUC MPPTI NAUGR JYATU IUVIO IAUOY EGSLE ATWAM NYQGR VUIOI TIGGS CPIKN HUYTV ENYHF PIOQT JEEEV HBVPF GRJPG UTAGH IDYAT FRPRP JPGPH FOQTT NOXNY CWTPP ECKGD JUOMA UCTJO EHGTU KNHNO XGRBP DMQWF TEWGR ZHEXO IOWTF UISCC FFTPH IOFOV VWIGT IGRXG HBFAH TAQJI OIPSQ BMGMC WTRWI DMLZP OUKCF FTICT GQRFX ESADS QPPHF JPTSC FGKCU JESQU UGRXC SSGPP TTJPG PPEMG STREF TPFGR TYESG DSQPQ KNHQF GVHFP EUYOS MBVVH PYIPU BVIMF OOSAL FCKUJ EOKTI KTNGA MNOGV HFREF TSETO QRIOI OGHWF TEJPT ICTEE AOFTI GYXGR FFRPR PJPGP HFJPO SFESQ FQTOY KMJVY UQOVT RBEKJ EAMNE EFIDM BVVHJ UPIQN FFIEP TFXEO TIOIA OFIUF IEPTH QTPXO JEENC IMLUT VFBKL FFISC NPWTP HTIGO GHIDG AOFSQ TIOVE EQFGF OXPTI GSUTE FVTPV HFFCV ROODU TVIOI TITOV IHUJE EQOSK HFCRE CVFTY XGISF SPWNE WPPPT BMIOI MZHIS UTTVE QKTXC SNQSU FEGKN JVEMA ATRLB UHJNO PMEEF OXPAO FIXCS TVAOF IOIIO CNJPC IQFXC TFTAC QVFCR BKSFF FMQOS EMEGE QHIMN EEYIU JCBDL FUDJT EDVLZ PEYVT PVHFD AUVES ABBPK PHTIG UQUWI KCIYA TQPFP WJVHF ZPPUE EYISK NHJEB TTKWM QGDJP TPOYN QUUJP PWNEK NHNIL GAKCC LJANO ESKMB DOVVT PFIFD UUKDJ FNUCN EKVFT YTNOX NYBPD DCRFH UMNYU QOLCS UGPCC CLQNU QDSAG SQUOF LPQKJ PGVRT PVHFG NEQFU JESQW JUAXV WPVRB FETOE OYIUJ SPOEG NOPTT JNETW PBRUN RAOFA MCRHG DSAES EHIQP TMYXJ AUVHF JEMNH BRPFP EEYHF TEJUD JEKBP DXJYJ UNUJI TRHPP EXQRL KNHVR BFIFQ HBDOV VTITE FAEBT SBIOE WRJPG UJEZG ASNYT GRWKC FKNPV IDGDU JAUVH FRLVI CBROO VHFJI HJPSG STWRF EHJNL FFWBV ESNOP RHBFD FXEMQ PFFAD TADMA OFWBU FBKLJ PGJVO MFDJE KBDOV VIUCT UJEUK MFCNE JETCI EJEEN OPMIO VOJVI HWETU HFFIE PTCGC BWSFK TXCST VIMNL JMEUJ ITVHF NATVT XQYFC RTYED CMFKN UQSFT VJEEJ VTIKS NQROK NHCNE KTBRP FFIUV OTGEJ HIUYA TQNUK GIVLZ NOOIS UQRZU HPTTJ VLJVE SCLMA EYRLP FEEPO XVHJU BVKLE KNHYA TCBPW TTVOS KETJI HJAOF WFYES GOONE WGLUJ EDJIM NESUF PTTIG AJTCP PDJVI PPESU WFTEP PTIGR PQFTQ BZVHF VINGT IGWBV ESKSP PLFXE MKTTT EBNLZ JIHJP SGSTW RFYHF PTIGC BRRVR TVTEE YAUGR DCMFQ UUUOI CRECN EHATV TICTJ VSIQT UJEDQ NDTEU GFMQO SVIMG WFKGI KNHMG BVLFC SUWPP HFUJE GNOPT AOFKJ EKFFI UWPUQ AEGGS GEBPG MGTVT NJPGU JETKN HNECN ATVOG YAUGR JPTPC HJIHQ TETUU SGSQT IOMLF TWIKC INICG RBNLZ FOVUE EVHFH ISUTU JRFGR BEKTY IUJWB VESVH FHISU TUJRF GRBEK TEOOV AJPEE VHFRR JOASA AOFBB EKVRC PTEWQ IDGSX KTDJE THOSV HFEON RAOAF PTTIG EOVIS GSUCT FAEQK CPWLE PTDCL MFIDM BFEAV UEBNL NQBJN ETGRW KCFUA OFMPU TGKXF FLJPE TGRWK CFUFP TTICT DCRSK ESYES GDPYN UJETW BGNOP TSMQW MAFJN LFFUQ YIUJW BVESV ALKNH QUUTA DMSPP ECAOO GATKT IKTUJ EJTPP YESEO OPEDV IPPSB NLUJE DQPQG RDCBM KNHWN EGRUJ EGNOP TWBUR VKNFF HVPDS GDTKF OQTUJ OVUAO FSPHI OVEST ADMPB VCIGS BNLEG AEVHB PKGWL MAIUJ AEUTP RPFFC NUHZQ FTRIM NIOIO WGRJP TPVHF WPTDA UVESA BBPKX JIDJW PWLEJ AWGKJ NLFFM FKNTV AOVLZ DYTJE FTLVE KQTEQ CRBVI PPOVT RBEKX CSTCF FYEXG RFVHF OOTVU QJIMN OOVHF UUCHL PQRBP DJJAE OAEGS VTEUJ AUYHF POVTP PYESY ATKNT VAMNE EVHBV IHQTB CSDTE XKNXC TFTPS QOGEO OPEDV OSCNE CLUJO VIHJV WBUWF VWFYE SGVFT YNWCI UTJNL PRESC TJPGB PDTVI MNOON IOGTI GDDKS OQLPP GFTOQ GRBVI OIATC RERAS VYSQO NCNEN IUGRB NLZGV FTYDW SUQMF THBUM PXEEQ UUPEY VTJOE JEAMN EEKNT QMFQN FGLTG AOUWF TEEFI DMSQJ OOGAO FIOVR PFUDG DIKMT GLGCS UJEOG WGCCJ NIUAM BPAHG RJVOM FHJOI OGEEG DUQGF VSPOE GKBSG PBVCI KNHKN TVAMN EEVOB POUJE SHLPQ RPHTI GBVKL EKNHC NEVHB VIEUT BTTFF TIGPS QCFUS XKTIF IDMBV VDJFN UIEUC RFUPP PSFVO NALBU TFOAJ NNFYD JEKPJ OLCYU JAOMS GQRMG TUKNH OELPO XKLMN OPMIO VOJV', 0)
    test.start()





#
#
#
#
