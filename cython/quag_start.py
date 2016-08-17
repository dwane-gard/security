# Decodes a running cipher
from packages.pad import Decode, Encode
from packages.analyse import NthMessageQuag, NthMessage, ChiSquare, QuagFrequency
from packages.pre_analysis import Kasiski
import itertools
import multiprocessing
import time

class Quag:
    def __init__(self, cipher_text, degree):
        self.cipher_text = cipher_text
        self.cipher_columns = []
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

        self.decoder = Decode(self.cipher_columns[0])
        self.alpha = [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        # self.keys = itertools.product(alpha, repeat=degree)
        self.degree = degree

    def pre_analyse(self, cipher_text, degree):

        result_alpha = []
        cipher_columns = []
        j = 0
        while j < degree:
            i = j
            nth_cypher_text = ''
            while i < len(cipher_text):
                nth_cypher_text += cipher_text[i]
                i += degree
            j += 1
            # print(nth_cypher_text)
            cipher_columns.append(nth_cypher_text)


        # returns the best guess if it is significantly better
        objective_plain_text_columns = []
        objective_keys = []

        # Returns the best guess
        plain_text_columns = []


        for each_column in cipher_columns:
            quagFrequency = QuagFrequency(each_column)
            initial_alpha = [0] * 26
            # new_decoder = Decode(each_column)
            # plain_text_columns.append(new_decoder.quag_breaker([getattr(quagFrequency, i)[x].letter for x, i in zip(initial_alpha,self.alpha)]))

            objective_key = [getattr(quagFrequency, i)[x].letter if (getattr(quagFrequency, i)[x].chi*50 < getattr(quagFrequency, i)[x+1].chi) else '.'
                            for x, i in zip(initial_alpha,self.alpha)]
            #
            objective_key = [getattr(quagFrequency, i)[x].letter
                            for x, i in zip(initial_alpha, self.alpha)]

            objective_keys.append(objective_key)


        # manually changing the alphabet with letter gleemed from the statistical anaylsis
        # and anaraming letters close to it
        objective_keys[0][10] = 't'
        objective_keys[1][8]  = 'h'
        objective_keys[2][22] = 'e'
        objective_keys[2][14] = 'a'
        objective_keys[3][18] = 't'

        # Statment
        objective_keys[1][4] = 't'
        objective_keys[7][18] = 'n'
        objective_keys[8][13] = 't'

        # None
        objective_keys[4][19] = 'n'

        # good probabioty tells
        # objective_keys[1][18] = 'o'

        # objective_keys[4][18] = 'o'
        # objective_keys[5][21] = 'o'

        # objective_keys[6][14] = 'e' doubles up

        # objective_keys[8][22] = 'o'


        # # gueesing

        objective_keys[0][18] = 'm'
        objective_keys[1][24] = 'a'
        objective_keys[2][16] = 't'
        objective_keys[3][23] = 'h'
        objective_keys[4][16] = 'e'
        objective_keys[5][5] = 'm'
        objective_keys[6][6] = 'a'
        objective_keys[7][12] = 't'
        objective_keys[8][16] = 'i'
        objective_keys[0][3] = 'c'
        objective_keys[1][25] = 'i'
        #a fits
        objective_keys[3][7] = 'n'

        objective_keys[3][3] = 'f'
        objective_keys[4][24] = 'a'
        objective_keys[5][5] = 'm'
        objective_keys[6][0] = 'o'
        objective_keys[7][8] = 'u'
        objective_keys[8][0] = 's'

        objective_keys[4][20] = 'f'
        objective_keys[5][16] = 'r'
        objective_keys[6][10] = 'e'
        objective_keys[7][13] = 'e'
        objective_keys[8][4] = 'm'
        objective_keys[0][5] = 'a'
        objective_keys[1][21] = 'n'
        objective_keys[2][11] = 'd'
        objective_keys[3][0] = 'y'
        objective_keys[4][25] = 's'
        objective_keys[5][15] = 'o'
        objective_keys[6][25] = 'n'

        objective_keys[7][15] = 'w'
        objective_keys[8][2]  = 'a'
        objective_keys[0][23] = 's'

        # a fits
        objective_keys[2][3] = 's'
        objective_keys[3][9] = 'k'
        # e fits
        objective_keys[5][11] = 'd'

        objective_keys[6][21] = 'w'
        objective_keys[7][6] = 'h'
        # a fits
        # t fits

        #
        objective_keys[1][23] = 'd'
        objective_keys[2][15] = 'o'

        # y fits

        # objective_keys[8]




        # objective_keys[3][3] = 'f'
        #
        # objective_keys[4][24] = 'i'
        # objective_keys[5][5] = 'l'
        # objective_keys[6][0]  = 'e'
        # objective_keys[7][8] = 'h'



        # objective_keys[5][5] = 'm'
        # objective_keys[6][6] = 'a'
        # objective_keys[7][12] = 't'
        # objective_keys[8][16] = 'h'

        # objective_keys[0][1] = 's'
        # objective_keys[1][24] = 't'
        # objective_keys[2][0] = 'u'
        # objective_keys[3][22] = 'd'
        # objective_keys[4][16] = 'e'
        # objective_keys[5][21] = 'n'

        # objective_keys[3][3] = 'w'
        # objective_keys[4][24] = 'i'
        # objective_keys[5][5] = 'd'
        # objective_keys[6][0] = 't'
        # objective_keys[7][8] = 'h'
        #
        # objective_keys[8][0] = 'a'

        # objective_keys[3][19] = 'u'
        # objective_keys[4][18] = 'n'
        # objective_keys[5][19] = ''
        print([str(x) for x in range(0,25,1)])
        for objective_key, cipher_text_column in zip(objective_keys, cipher_columns):
            print(objective_key)

            quagFrequency = QuagFrequency(each_column)
            new_decoder = Decode(cipher_text_column)
            objective_plain_text_columns.append(new_decoder.quag_breaker(objective_key))

            plain_text_columns.append(new_decoder.quag_breaker(
                [getattr(quagFrequency, i)[x].letter for x, i in zip(initial_alpha, self.alpha)]))

        plain_text = [None] * len(cipher_text)
        k = -1
        for each in objective_plain_text_columns:
            i = k+1
            j = 0
            while i < len(cipher_text):
                plain_text[i] = each[j]
                i += self.degree
                j += 1
            k += 1

        derp = (''.join(plain_text))

        print([derp[i:i+9] for i in range(0, len(derp), 9)])
        print(derp)
        exit()



    @staticmethod
    def list_duplicates_of(self, seq):
        location = []
        for each_letter in set(seq):
            start_at = -1
            this_letter_location = []
            while True:
                try:
                    loc = seq.index(each_letter, start_at + 1)
                except ValueError:
                    break
                else:
                    this_letter_location.append(loc)
                    start_at = loc
            if len(this_letter_location) > 1:
                location.extend(this_letter_location)
        return location

    @staticmethod
    def analyse(self, plain_text, key_alpha):
        chiSquare = ChiSquare(plain_text)
        chi = chiSquare.output()
        ic = chiSquare.ic
        # print('%s | %s | %s' % (str(key_alpha), str(ic), str(chi)))
        if chi < 200:
            print('%s | %s | %s' % (str(key_alpha), str(ic), str(chi)))
            # print(plain_text)
            with open('quag_result.txt', 'a') as results_file:
                results_file.write('%s | %s | %s | %s' % (str(key_alpha), str(plain_text), str(ic), str(chi)))

    def start_single(self, cipher_text, degree):

        # print(degree)
        key_alphas = self.pre_analyse(cipher_text, degree)

        full_plain_text = ''
        cipher_columns = []
        j = 0
        while j < degree:
            i = j
            nth_cypher_text = ''
            while i < len(cipher_text):
                nth_cypher_text += cipher_text[i]
                i += degree
            j += 1
            # print(nth_cypher_text)
            cipher_columns.append(nth_cypher_text)

        pairs = zip(key_alphas, cipher_columns)
        for each_pair in pairs:
            decoder = Decode(each_pair[1])
            plain_text = decoder.quag_breaker(each_pair[0])
            full_plain_text += plain_text + ' | '
        self.analyse(full_plain_text, ['A'])
        print(full_plain_text)



        # for each_alphabet in itertools.permutations(self.alpha):
        #     # print(each_alphabet)
        #     decoder = Decode(self.cipher_columns[0])
        #     plain_text = decoder.quag_breaker(each_alphabet)
        #     self.analyse(plain_text, each_alphabet)

    def start(self):
        ''' MultiCore '''
        q = multiprocessing.Queue(maxsize=50)
        jobs = []

        # Create workers
        for i in range(0, multiprocessing.cpu_count(), 1):
            p = multiprocessing.Process(target=self.worker, args=(q,))
            p.start()
            jobs.append(p)

        # Feed items into the queue
        for each_alphabet in itertools.permutations(self.alpha):
            q.put(each_alphabet)

    def worker(self, q):
        while True:
            if q.empty():
                time.sleep(1)
            try:
                each_alphabet = q.get(timeout=1)
                print(each_alphabet)
                plain_text = self.decoder.quag_breaker(self.cipher_columns[0])
                self.analyse(plain_text, each_alphabet)
            except:
                break
        return

if __name__ == '__main__':
    cipher_text3 = open('cipher_3_text.txt', 'r').read()
    cipher_text3 = ''.join([x for x in cipher_text3 if x.isalpha()])
    test_text = ''.join([x for x in '''
    RDAJR TQCXS GPQTF ONWNP SWRDD OQCME PSDYG PLKBU FEPNR DBEZB VCCOG NJOOT
     CRRND RWMFE SNAGQ YOEBJ SAOWC FCPXS JMBCR ZGIQC SAOYC SGADR GEZBC MCPPM
     JHOPB WXEZE EMHEX CBYBV FBGOS EPXSD DFJTO OHTOZ VBPNI BGRDC PDHRQ YRBBV
     CRFMR PORJE PNXKB EZBAO QOXZI WNOZE IMORO YJSOM PUXAM BBEJS FFASF FFARD
     ROQHC OFRQB OZCRB ORKWZ DCQZS AOVQT IDATF RCOBM FTOSS DQFQH XUJTR NAQHV
     ONOZS OQHMY NMDRG SCBFU CDHES DFOMB QTSAO DAIQN LFORD UFMTP HZSKP CAGOZ
     SCLAD SGTAW LMDRF HAWQF BHFFO PPJRT EPJJN EDORN CJTPE COECN RZXAQ YASTO
     DXUVQ BTEHR QYVEP NSDGG VKGLR GEOBC XZIJH VGBNO VBIMQ NQDSG XEJBF HASOC
     UKTMN DJPGE LDQBD FJROO TRUVI KGPBB DFJPA MNTGO QBTMJ VORZE BZACF PNHGL
     JSNPR GRFRB UPBDG OHIEF RTEPS KQZVK GLCCU MQPOO OCOHZ DUONT ZZCWN OVTQO
     OBEPS BFPJH OBTKC YAOGV AEPHD YFLDV XZIYQ FQTID ATQZU KUMCD ELGNX ECJOE
     OKTET RODCD VEAOG VMBFH AJOEF UFECN OCRWN ODROC APOPS DVTAO UMQSJ VSAPO
     NJGVF MOEZK FECRX MRDVE ZBFMS YCMRD VVRSH MRSQP NYJPX KWMSE TPBCV CCNRZ
     CCUMQ JOZSC OYDOJ LCSDF JTOQJ TGMQE BSMBR ZQKWL SDVTS AOQDT UOASB EBKZM
     SAREJ EFXAH VOQAX DDHUC ASFEA COAZD BMNUA QARGO UBEVH YGLAE TRCUB EZEGM
     RTNPS AOLDS GORPO PLWXE ZEAPF AXZAF OTCRO CAETL JOWPN EWMNT OEFKN PUBFO
     MBOIO BEVAO TMZEB SBKBU SAODA TLAAS QTFUF ECNOC RAQHA VOCSA XDFEP NVEFU
     CKBUS DSMDC XESCO SJIVM QBBEJ SCMNT QGARA VNUGM RWXEZ TNVRJ HJVBP NFEPN
     ZKAYQ SAVSA GCXKB USDWM SAXDS VFMSG QZNBT EAHGO SAOSJ JXEDC SOWPE OOBEN
     XSQLA GQFBH EMFBX GAECV FTHCA OQNTG ZLAWR DIBGE JOWRB BRCBY VCTSG CDTOS
     EYGLA WNOBB QCGBR NDOUD SEEEA HSNDN XZINO TCRBO SFOVN JRQBB GOGDA JKDSA
     QDCMQ CLLCW XHDSH DACOD RBGRV AREAV OCBKZ MJSRV GKIMG BRNSW XEZTN VRFOT
     CRODC KGCJB UYXFO DSOQE SDGPL BXEOB EDCOR NBYSF SBIMN THPBC LVZEU ECEFX
     ZKAVH WORCU PSEDQ XDSOC UKTMS BTLSD GLAAQ YAETO TRGMR YTPBC GOIBG LJSGG
     VDEXJ OWRCR EMFTP JTOVO QTHZD TONXD HCEDQ XJOWR DCOZG EEHDS FLCWX ZIEBP
     OPQVN TAMNT UPXSQ FSTNP SSJLA ONMGR QAOBU EZKFO NNOSC OGQCT NMQSO ZGKBU
     DJQSG EAZSB TLNKT VDOSM FEHDA KPNEB UMDHS JSAOZ JNRZG TIVRT NMCOP JSAXZ
     IKNPU BPMHT RCAYQ FQBRN BYWOJ OWECN RXANO HDKGT CRREA GNVJO FEDOG NXION
     SFRSJ NOPNK IMZBR CGBIM QYTOM PPPJO GVNTN MEDQX DSGOV ALAAD CNAHQ ZSWRZ
     STQHD KGTCR REAGN QTTGL JSQZA MXZGD VUCTG OMBXY JOAJM KUDRD NONBF EBYXR
     DOGMU BBVME WVNBN OVKGY TSGTA BPECU GEARG LCSOH CRUDR DXDOD ZMVKG LMYFF
     OBEGJ SQCVA QDDKU EZBLS RBOVH WORCU PSIBG DCNOO NBQFS BRCBK OCEUG HAGQF
     BHBEO RQYJS OPNYG LJOWD CKPMS NEDMK GLLOQ HDOUL AWRDO ROSJG GPECL ZCTIM
     QYNPO PLHJT NYXEB DVBEP STNPS PQVNT XEDCA ORTFO TOUMG CXXAA ODSEE EAHGO
     FRLPN HJMNT XZSDN OVAOL DSBOH EAVBY PMHTR ZGOQT QKOZG SGLDT TOMBI VRKGE
     ZKFHD SRTSB EVDSZ MGKVE ZBEMV EFPNY QZAKB LJSSF JCUVN JGLDT AVIAG QAESN
     ATQLA CCYDO XTACG EAREV ECODC KGOCM XETPQ ZMYFM BIGOD SZYQS AVSAX TJGQF
     BHCPX EIVRK GLACX GAHXZ DSAPB CTVSY QGARV CCNJL AROVV EFZCT IMQYV PQTQS
     QKIMZ BJPRE PVSTP MRAQR LBUVV EFHJC PVNJG OGDGL JSSFS SQFNH OSSAR ZLIHN
     JWRDV KPNJO WECGQ YADHE DOULA CCLJN CMQSQ ZDCPJ RDXLA EUOUB EUATG OSAOC
     ASXSA OTMDO UYABG LJNJV SAXZR BTONH FVZEU EZBTP ECOCT OBVNJ RUDKB DJNCN
     AKBAT TTLDO WMDOU MUBBQ QDHUZ TNVME FVMPP VHKOS QBAOS BVOQA XDRBG ECPSO
     WTQPU DXSSA XDORQ QBBAV NTNMH UGFQB GLDTF HZBBL ASGPQ TOSFR LVNJN MIDOD
     JOGOZ DJLAA RDNTR RSURN BYFAC MOZCR EMDCP JJOGM QETEA HJVSA RZXDB MHDEJ
     AEEDZ BWPUB AMDAH UDOUE CCUYA AQHSA RZLIH NZBJP RTNPS KTPMB QFSEB SZBPA
     AHNVM EBSSD PSMBN OVSQC QYNMV EFTCR SMJOW DCNOP NBRCB KOCCO XDDKU VSWRD
     NDCCC FPMME BSJWR DZECA XTQLA CCPNH GLDTJ PRKGV BBVEV BOXRC REARA JRUCM
     QVXDC RTOMB FECNL SASZP NHRDL SAMJI XRCUP SFDAM RPOPL WXEZA OCHDE PEKGP
     EDHED ORRFD HZSIQ CMRFY JTNET RBDCU GLASO ZSTNM FESNA GQYOE BJDCO ESBEO
     TTPVN KBUZD JEZEB XHUPL AWRDH DELAC CVNJN VMWXE ZAXDJ SFFAE BSZDJ VSROP
     BCLYD HOPND PSMEB LDPCJ DJRVN IQCCO TMJOR GARLN COWEJ NOEZB PMSTO CVEFT
     QEAMG EBSOU GONDH CHRQZ SBBEQ EBRAT QCATR VBKWF ASFEZ BAOQE POHTN VRSGO
     QYXDN DAPST OCZDJ ZDSGJ RDAMC OOVRT QJCUQ GARGL APNON BFOMB GVMBF EZBLC
     AOQED CJPXS REARE VECOA ARFON EBSKU FEIDX ZITNC CUWLD CQEJS GVBCG LJOZP
     EDHEM RFYJT NOFGR DJDBP BCLHZ BBVIB GEZDF MNEFE XGHDS DAMQS RZGKG YDMOD
     MBVMA CRNJT GNAFO ESBEP NYJPX TNPNM FTCRE MDHXZ ILHDS TNOTJ NEJHF LDROL
     CWGLJ SQZAG RNBGN PNJOS MYQFS CQOLD BNJIO
    ''' if x.isalpha()])

    # running.start()
    # quag.start()
    test_quag_text = ''.join([x for x in '''
IBWVUPLTP  JTKPPMYCT  DVXYGNYQY  NTWNFSUIX  NACXCFTGV
AIKPSRTCO  JJWPRRVOL  AAARURJNU  IXMXPQBVU  IBWOGPCDP
LNNRDFPSL  IBUGOCDOT  WKCPIRQRV  QGYGCXLVM  NOBEQFVOL
GBWGPATNJ  LYWRMWEKL  AAVICVEAQ  BKUVFJURD  VIOZMPTZO
VSLIHQBQX  FLLLWHPUS  GVXP
''' if x.isalpha()])

    # for degree in range(1,18,1):
    quag = Quag(cipher_text3, 9)
    quag.start_single(cipher_text3, 9)
        # quag.pre_analyse(cipher_text3, 9)
    time.sleep(10)
