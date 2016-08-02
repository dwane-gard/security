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

#
#
        for each_column in cipher_columns:
            column_result_alpha = []
            quagFrequency = QuagFrequency(each_column)

            derp_alpha = [0] * 26
            derp_alphas = [derp_alpha]

            running = True
            count = 0
            delete_these_alphas = []
            while running is True:
                for each in delete_these_alphas:
                    derp_alphas.remove(each)
                delete_these_alphas = []

                for each_alpha in derp_alphas:
                    # # create actual alphabet for key, Check for dupliucate items
                    # print(each_alpha)
                    if len([getattr(quagFrequency, i)[x].letter for x, i in zip(each_alpha, self.alpha)]) != \
                            len(set([getattr(quagFrequency, i)[x].letter for x, i in zip(each_alpha, self.alpha)])):

                        for each_letter in self.alpha:
                            duplicates = self.list_duplicates_of([getattr(quagFrequency, i)[x].letter for x, i in zip(each_alpha, self.alpha)], each_letter)
                            # print([getattr(quagFrequency, i)[x].letter for x, i in zip(each_alpha, self.alpha)])
                            if len(duplicates) > 1:
                                for each_duplicate in duplicates:
                                    # print('Checking for duplicates: %s' % str(each_letter))
                                    working_with_duplicates = each_alpha
                                    if working_with_duplicates[each_duplicate] < 25:
                                        working_with_duplicates[each_duplicate] += 1
                                    else:
                                        # maybe should ditch it here
                                        pass
                                    # else:
                                    delete_these_alphas.append(each_alpha)
                                    derp_alphas.append(working_with_duplicates)
                                    break
                                    # print(derp_alphas)

                    else:
                        # print('this one is perfecet')
                        # print(each_alpha)
                        if [getattr(quagFrequency, i)[x].letter for x, i in zip(each_alpha, self.alpha)] not in result_alpha:
                            result_alpha.append([getattr(quagFrequency, i)[x].letter for x, i in zip(each_alpha, self.alpha)])
                            # time.sleep(2)
                        delete_these_alphas.append(each_alpha)


                break
            # result_alpha.append(column_result_alpha)
        return result_alpha

    def list_duplicates_of(self, seq, item):
        start_at = -1
        locs = []
        while True:
            try:
                loc = seq.index(item, start_at + 1)
            except ValueError:
                break
            else:
                locs.append(loc)
                start_at = loc
        return locs

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
        for each in key_alphas:
            print(each)
        # exit()
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
    for degree in range(2,18,1):
        quag = Quag(cipher_text3, degree)
        quag.start_single(cipher_text3, degree)
        # quag.pre_analyse(cipher_text3, 9)
        time.sleep(10)
