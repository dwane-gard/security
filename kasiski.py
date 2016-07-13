import functools
from suffix_tress import SuffixTree
import co_incidence_index
import brute_force_vigenere

class Kasiski:
    '''
    THIS IS NOT KASISKI  but ic examination at the nth character

    Uses Kasiski's examinstation to discover the key length for a vigenere encoded message
    Think the max might be set at 8 unsure and should be reviesd if this accours
    '''
    def __init__(self, cipher_text):
        cipher_text = cipher_text.replace(' ', '')
        cipher_text = cipher_text.replace('\n', '')
        self.original_cipher_text = cipher_text
        self.cipher_text = self.original_cipher_text
        print(len(self.cipher_text))
        self.multiples_list = self.factors()
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.alphabet = [x for x in self.alphabet]
        # if not self.multiples_list:
        #     self.multiples_list = [x for x in range(0, 15, 1)]


    def analyse(self):
        '''
        Analyse the cipher text to find repeating strings
        :return:
        '''
        import collections
        import itertools
        all_possible_substrings = []
        x = 1


        while x < len(self.cipher_text):
            x += 1
            j = 0
            # print(x)
            while j < len(self.cipher_text):
                substring = self.cipher_text[j:j+x]
                # print(substring)
                if 3 < x:
                    break
                all_possible_substrings.append(substring)
                j += 1


        sorted(all_possible_substrings)

        all_possible_substrings = (collections.Counter(all_possible_substrings))
        print(all_possible_substrings.most_common())
        return

    def finding_the_key(self, key_length=9):


        j = 0
        while j < key_length:
            i = j
            nth_cypher_text = ''
            while i < len(self.cipher_text):
                nth_cypher_text += self.cipher_text[i]
                i += key_length
            # print(nth_cypher_text)
            checkIC = co_incidence_index.CheckIC(nth_cypher_text)
            checkIC.run()
            checkIC.print_ic()
            # decoder = brute_force_vigenere.decode(nth_cypher_text, 0)
            # decoder.start()


            j += 1



    def output(self):
        '''
        Returns the calculated multiples
        '''
        return self.multiples_list

    def factors(self):
            '''
            Gets the factors of the length of the cipher text
            :return:
            '''

            n = len(self.cipher_text)
            return(list(set(functools.reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))))

class RealKasiski:
    def __init__(self, cipher_text):
        return3
    def run(self):
        return
    def output(self):
        return

if __name__ == '__main__':
    another_cipher_test = '''
    HQCNPXQNRHPRPGJPLOGQEVSIEILNOVQVSQTPCVUDLOGMPGZJPMNVLRFBFGZJ
HZFIHSQTFHMEVIEFESPOLGZJFWXCOHGZJHZVMIEFMPKVUYZVOAJVTRITZBLV
FACGREPLFYWIVANKYKHWICNLCZDQQTQEVTQYNBIQFFNMCKVICPVNWFTWKJMS
KTRPOFWJSNP
    '''
    cypher_text = '''
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
    # cypher_text = 'abcdeknfdslkgnadsklfnlksabdabdbadbbadnscklzmcklznclabcabc'
    kasiski = Kasiski(cypher_text)
    print(kasiski.cipher_text)
    for each in range(1, 18, 1):
        print('Key length %d' % each)
        print(kasiski.finding_the_key(each))
    # kasiski.analyse()
    # print(kasiski.output())
