from brute_force_vigenere import decode
import time
import multiprocessing
import itertools
from functools import reduce
from co_incidence_index import CheckIC


class AutoKeyDecoder:
    def __init__(self, cipher_text, key_length):
        self.cipher_text = cipher_text
        self.key_length = key_length
        self.possible_sequences = itertools.product(range(0,26,1), repeat=self.key_length)
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z']

    def run(self):
        '''
        Runs the program, manages the multithreading
        :return:
        '''
        q = multiprocessing.Queue(maxsize=50)
        jobs = []
        pool = False
        multithread = True
        if multithread is True:
            if pool == True:
                m = multiprocessing.Manager()
                ze_pool = multiprocessing.Pool(multiprocessing.cpu_count(), maxtasksperchild=5000)
                ze_pool.imap(self.auto_key_decoder, self.possible_sequences, chunksize=1000)
                ze_pool.close()
                ze_pool.join()
            else:
                # Create workers
                for i in range(0, multiprocessing.cpu_count(), 1):
                    p = multiprocessing.Process(target=self.autokey_worker, args=(q,))
                    p.start()
                    jobs.append(p)

                # Feed items into the queue
                for each_item in self.possible_sequences:
                    q.put(each_item)

                # Wait for each worker to finish before continueing
                for each_job in jobs:
                    each_job.join()
        else:
            for each_possability in self.possible_sequences:
                self.auto_key_decoder(each_possability)

    def auto_key_decoder(self, key_num):
        '''
        Builds the key and runs import decoder modules, analyse module etc
        :param key_num:
        :return:
        '''

        # Build key
        key = ''
        for each_char in key_num:
            key += self.alphabet[each_char]

        # Run decoder
        decoder = decode(self.cipher_text, 0)
        message = decoder.autokey(key)

        # analyse results
        self.analyse(message, key)

    def autokey_worker(self, q):
        '''
        Used with 'Process' multithread message
        :param q:
        :return:
        '''
        while True:
            if q.empty():
                time.sleep(1)
            try:
                obj = q.get(timeout=1)
                self.auto_key_decoder(obj)
            except:
                break
        # print('ending worker')

    def analyse(self, check_this_message,key):
        '''
        Analyses results using an incedence co-effient check

        :param check_this_message:
        :param key:
        :return:
        '''

        ''' Ze IC '''
        IC = CheckIC(check_this_message)
        IC.run()
        ic = IC.ic
        # print('%s | %s' % (key, check_this_message))
        print('%s | %s' % (key, str(ic)))
        if ic > 0.06:

            with open('autokey%sresults.txt' % self.key_length, 'a') as results_file:
                results_file.write("%s\n%s\n%s" % (str(key), str(ic), str(check_this_message)))
                print('%s | %s' % (str(key), str(ic)))
                print(check_this_message)
                # time.sleep(10)

cipher_text = '''
DSQBJHCHVOXWXGASLPKJXGM
''' # key=SECRET
real_cipher_text = '''
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
PHHER RU'''
if __name__ == '__main__':
    for key_length in range(4,9,1):
        print('[key length] %s' % key_length)
        autoKeyDecoder = AutoKeyDecoder(real_cipher_text, key_length)
        autoKeyDecoder.run()

