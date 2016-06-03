from co_incidence_index import CheckIC
from corpus_analysis import Analyse
from transpositional import Trans
from brute_force_vigenere import decode
import chi_square
import time

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

class DecodedMessage:
    def __init__(self, Decoder):
        self.best_guees = None
        self.second_guees = None
        self.third_guees = None
        self.messages = []
        for each_letter in [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']:
            self.messages.append(self.EachMessage(each_letter, Decoder))

    class EachMessage:
        def __init__(self, shift, Decoder):
            self.shift = shift
            self.plain_text = Decoder.run(self.shift)
            self.chi = chi_square.CheckText(self.plain_text).chi_result

    def run(self):
        for each_plain_text in self.messages:
            if self.best_guees is None:
                self.best_guees = each_plain_text
            elif each_plain_text.chi < self.best_guees.chi:
                self.third_guees = self.second_guees
                self.second_guees = self.best_guees
                self.best_guees = each_plain_text
                # print(each_plain_text.chi)
                print(self.best_guees.chi)
            elif each_plain_text.chi < self.second_guees.chi:
                self.third_guees = self.second_guees
                self.second_guees = each_plain_text
            elif each_plain_text.chi < self.third_guees.chi:
                self.third_guees = each_plain_text

        print('*'*20)

def breakup_into_nth(cipher_text, key_length=36):

    # Build the de-shifted text that is the best gueess from chi-squares
    j = 0
    cipher_text = ''.join([x for x in cipher_text if x.isalpha()])
    list_of_answers = []
    plain_text = [['.'] * len(cipher_text)]
    while j < key_length:
        i = j
        nth_cypher_text = ''
        while i < len(cipher_text):
            nth_cypher_text += cipher_text[i]
            i += key_length
        decoder = decode(nth_cypher_text, 0)
        workingDecoder = DecodedMessage(decoder)
        workingDecoder.run()
        list_of_answers.append(workingDecoder)
        j += 1

    # build the key used to make the best guees
    m = 0
    key = [['.'] * key_length]
    for each in list_of_answers:
        k = m
        key[0][m] = each.best_guees.shift
        for each_letter in each.best_guees.plain_text:
            plain_text[0][k] = each_letter
            k += key_length
        m += 1

    return ''.join(plain_text[0]), ''.join(key[0])


for each in range(9,180,9):
    print(each)
    de_shifted_text, key = breakup_into_nth(cipher_text, each)
    print(de_shifted_text)
    for each_key_size in range(1,9,1):
        trans = Trans(de_shifted_text, each_key_size, str('Shift Key: %s' % key))
        trans.create_possible_answers()

    time.sleep(5)






