from pad.pad import decode as decode_cy
from check.analyse import WordSearch as WordSearch_cy
from brute_force_vigenere import decode as py_decode
from word_search import WordSearch as py_WordSearch
import itertools
import time
import multiprocessing


'''
first cython build
cy time: 0.7430474758148193
py time: 0.9128749370574951

'''
'''
moved the words list so it is only intialized once
cy time: 0.6541030406951904
py time: 0.8258819580078125

'''
'''
run compatability on word list once
cy time: 0.3932199478149414
py time: 0.45741724967956543
'''
'''
more compatability ot word list ran once
cy time: 0.3907437324523926
py time: 0.39853334426879883
'''

class Runner:
    def __init__(self):
        cipher_text = '''
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
        PHHER RU
        '''

        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                         'U', 'V', 'W', 'X', 'Y', 'Z']

        cipher_text = [x for x in cipher_text if x.isalpha()]
        check_len = 8
        cipher_text = cipher_text[0:check_len]

        self.cy_decoder = decode_cy(cipher_text)
        self.py_decoder = py_decode(cipher_text, 0)

        self.cy_wordSearch = WordSearch_cy()
        self.py_wordSearch = py_WordSearch()

        self.keys = itertools.product(alphabet, repeat=check_len)
        print(cipher_text)

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
        for each_item in self.keys:
            q.put(each_item)

        # Wait for each worker to finish before continueing
        for each_job in jobs:
            each_job.join()

    def worker(self, q):
        while True:
            if q.empty():
                time.sleep(1)
            try:
                obj = q.get(timeout=1)
                plain_text, key = self.cy_decoder.runner(obj)
                words_len = self.cy_wordSearch.run(plain_text)
                if words_len > .7:
                    print('%s | %s' % (str(key), str(words_len)))
                    with open('cython_results.txt', 'a') as results_file:
                        results_file.write('%s | %s | %s\n' % (str(key), str(plain_text), str(words_len)))
            except:
                print('[!] run finished')
                break
        print('ending worker')
        return

        # for key in self.keys:
        #     cy_start = time.time() # for testing
        #     plain_text, key = self.cy_decoder.runner(key)
        #     words_len = self.cy_wordSearch.run(plain_text)
        #
        #     if words_len > 0.7:
        #         with open('results.txt', 'a') as results:
        #             results.write('%s | %s | %s' % (words_len, plain_text, key))
        #
        #     ''' Testing code '''
        #     print('cy time: %s' % (str(time.time() - cy_start)))
        #     #
        #     # py_start = time.time()
        #     # py_plain_text = self.py_decoder.decrypt(key)
        #     # py_words_len = self.py_wordSearch.run(py_plain_text)
        #     # print('py time: %s' % (str(time.time() - py_start)))
        #     #
        #     # print(words_len)
        #     # print(py_words_len)

runner = Runner()
runner.start()