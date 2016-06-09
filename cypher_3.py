from co_incidence_index import CheckIC
from corpus_analysis import Analyse
from transpositional import Trans
from brute_force_vigenere import decode
import chi_square

import multiprocessing
import time
import itertools
import numpy as np

first_text = 'KIWDY FAIAS YQXQF GMQ'
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
PHHER RU
'''

test_text = '''KICOSVYIIBFFGCYRAYDZVBSLDPCEIVQXFGEKB'''

class NthMessage:
    def __init__(self, nth_cypher_Text):

        self.cypher_text = nth_cypher_Text
        self.plain_texts = []
        Decoder = decode(self.cypher_text, 0)

        # For each shift posibility decode
        for each_letter in [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']:
            self.plain_texts.append(self.EachMessage(each_letter, Decoder))

        # sort each part by its chi of the english language
        self.plain_texts.sort(key=lambda x: x.chi)

    class EachMessage:
        def __init__(self, shift, Decoder):
            self.shift = shift
            self.plain_text = Decoder.run(self.shift)
            self.chi = chi_square.CheckText(self.plain_text).chi_result


class BreakupIntoNth:
    def __init__(self, cipher_text, key_length=9):
        self.cipher_text = ''.join([x for x in cipher_text if x.isalpha()])
        self.messages = []
        self.key_length = key_length
        self.multithread = True

    def run(self):
        # Build the de-shifted text that is the best gueess from chi-squares
        j = 0
        while j < self.key_length:
            i = j
            nth_cypher_text = ''
            while i < len(self.cipher_text):
                nth_cypher_text += self.cipher_text[i]
                i += self.key_length
            self.messages.append(NthMessage(nth_cypher_text))
            j += 1

        # get the nth best guesses and make possibilites from them
        possible_sequences = itertools.product(range(0, 5, 1), repeat=self.key_length)

        # Sorting causes memory issues
        # sorted(possible_sequences, key=sum)
        # print('[!] sorted')

        if self.multithread is True:
            m = multiprocessing.Manager()
            ze_pool = multiprocessing.Pool(multiprocessing.cpu_count())
            ze_pool.imap(self.check_posibilites, possible_sequences, chunksize=100)
            ze_pool.close()
            ze_pool.join()
        else:
            for each_sequence in possible_sequences:
                self.check_posibilites(each_sequence)

    def check_posibilites(self, each_sequence):
        check_this_message = ['.'] * len(self.cipher_text)
        key = ''
        whole_message = False       # Do we want to check the whole message or just the first n characters

        # build the message from its parts
        w = 0
        for each_guees in each_sequence:
            q = w
            l = 0
            key += self.messages[w].plain_texts[each_guees].shift

            if whole_message is True:
                check_message_length = len(self.cipher_text)
            else:
                check_message_length = self.key_length

            while q < check_message_length:
                check_this_message[q] = self.messages[w].plain_texts[each_guees].plain_text[l]
                q += self.key_length
                l += 1
            w += 1
        check_this_message = ''.join(check_this_message)

        # check if the entire message is close to englishness, if it is do furthur analisyis

        if whole_message == True:
            ze_chi = chi_square.CheckText(check_this_message).chi_result
            if ze_chi < 500:
                with open('results.txt', 'a') as results_file:
                        results_file.write("%s | %s | %s\n" % (str(ze_chi), str(key), str(check_this_message)))
            if ze_chi < 1000:
                print(ze_chi)
                print(key)
                print(check_this_message)
                for each_key_size in range(1,2,1):
                    trans = Trans(check_this_message, each_key_size, str('Shift Key: %s' % key), multithread=False)
                    trans.create_possible_answers()
        else:
            trans = Trans(check_this_message, 1, str('Shift Key: %s' % key), multithread=False)
            trans.create_possible_answers()


if __name__ == '__main__':
    for each in range(18, 27, 9):
        # print(each)
        # breakupIntoNth = BreakupIntoNth(real_cipher_text, each)
        # # breakupIntoNth = BreakupIntoNth(test_text, 3)
        # breakupIntoNth.run()
        pass
    breakupIntoNth = BreakupIntoNth(first_text, 9)
    # breakupIntoNth = BreakupIntoNth(test_text, 3)
    breakupIntoNth.run()







