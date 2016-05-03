import collections
# mono-alphabetic substitution cipher = each letter represents a difrent letter
# a transposition cipher. = plain text is reordered
# enigma machine

# Random IC = 0.0385
# Italian IC = 0.738

english = '''The world's largest oil and gas companies have addressed the nation's biggest liquefied natural gas (LNG) conference and predicted a bright future for the industry despite decade-low prices.

John Watson, the head of US oil and gas giant Chevron, said global demand for LNG was expected to grow by 35 per cent over the next two decades.

"To put that into perspective, that will be a doubling in LNG production as we meet the growing oil demand," he said.

"We will likely need as a world community a project the size of Gorgon every year for the next 20 years, so there is keen demand going forward."

Royal Dutch Shell chief executive officer Ben van Beurden agreed and said those predictions would be backed up by growing demand from developing nations.

"Market conditions are pretty challenging, but at the same time new markets are opening up. Markets like Thailand, Pakistan, Poland," he said.

"In the past these markets were simply too small for us to consider, but the rapid growth of floating re-gasification facilities amongst other things has considerably lowered the costs for importers and provided a lot more flexibility.

"This shows how important technological innovation is for the future of LNG."

Projects need to be 'smarter, not necessarily bigger'

A global oversupply of oil, falling demand and the uptake of renewable energy has driven prices to decade lows.

This has cost thousands of jobs across the world as companies slashed spending to remain in business.

Woodside chief executive Peter Coleman said he believed one of the answers could be phasing projects rather building mega developments.

"They need to be smarter, they need to be phased and they don't always need to be bigger," he said.

"We need to understand our customers and their future change in requirements and we need to be innovative and flexible in response and we need to be aggressive in developing new markets."

Media player: "Space" to play, "M" to mute, "left" and "right" to seek.
VIDEO: Extended interview with Ben van Buerden (The Business)
Mr Coleman's comments come just weeks after the company shelved its massive Browse LNG project off the Kimberley coast.

Today he indicated he would consider a phased development for the basin using floating LNG (FLNG) technology.

"I think we need to think differently about Browse and this just provides us an opportunity, this low point in the cycle to just sit back," Mr Coleman said.

"We are not under any development pressure. The market's not there for us at the moment so we don't need to go hard, we just need to be very sensible about it.

"FLNG is clearly the lead case."

But WA Premier Colin Barnet, who has long been at odds over the company's decision to abandon onshore development at James Price Point, is not so sure.

"You won't be able to commercialise those well enough with just simply floating LNG in my view," he said.

"I don't think we have seen the end of the big onshore projects but I think we probably have in the Carnarvon basin."

Shell is building the world's first floating LNG project for the Prelude field off the Kimberley coast.'''

cipher_text = '''
COOUS ULYDU TQOHY SEELP EUTST GTOAR
IDTHM WPEER DTTEF EXUTO ROSEC UYCOU
DUBEU LUONL IKFTE YHCER LROTU ESAOF
ANRAI EQSOR ETLER HTFTE UISEI SDQBY
LSFOS ERTIN NRGED AWTOR KLEQA IASNT
RFEXL OASMP TBOTW UHEER ISTWD EOIUL
ETASV LTAGI UYAST OTEAR PNOIN GNITI
HOEDY TETCR OTNQT IUPES ROKEY MNTLA
ITNKS HIITI OHNLC EYTDE ANNDH TREIG
ITNGO HTTOD OONAH DTTET LMLIO IOENS
LDLAO ORFSY DMEFS ARUOM ILNGO LEENR
OSCKO TBNEF HEECA TORMP EYCLD DANRE
KARUY NPBTC UONDC FSTSU EANRM SOHNE
YLEEN OTPRA IIOND TFSUN RNEAH DCAHT
ETNET BFAIT OEMPS CAHNY LMOYW PEEES
OOSTI LTHHE TRIRN EERME VSINN AGTSA
OPVIE RDDER FITOI ELLOW MCECU OONNS
SEINI RCMAL NOIAC RWFHO ANFFT TOARD
YPTHE AEOIR GEYBS RINLL VIESI NTIED
UYRCA OONMP EYCAI BUNSE IEEVN LEBDI
ONNAT RNEDI NFANL ICSIA TTEMS AESNT
NAOTK MSIEE TNORV GEICO YRLON MSETI
TEMEU SNVTB OIBEV DLTIE ATTYE HOEUR
OPYEE LEMSD VEEMA RUSCH RTTHY EEFIR
SAOFD RHEAR KOMAG RKWIN ONNAO RNEDY
CRHIW IKUNO WOILV ULYNE ERADS RTEHI
IMLAO ANEDC NLTBT DEUBO EEDWI RIHTH
TBUNS ULTES AOREL UWYIL TNOHY GAIVE
NUAMD REOGO IWNAI NMOER HAISY NTCOR
NSEOS OFAIT SOEBN RUWSI CSRIA SMEIN
OSUHA YALVE NHCET ANCOW GRHTG IAONE
IEOUO GSRWR NGDEH IENDW YLOUT ENIET
EDLLR WOEVE LMLIA IOANM FYENS ORNON
LMOYW PEEES FRINI EAENC YLDET LVAAS
DTWHH EEANT MCPAE ONEYD RLEDK ABCAN
TUCYT PARND REREE ITHIR TEPLW NAMNS
WRIPU EEEDO DAENM NRTON ADNAO ESATR
IOCAO MLNPR DIURT TIFNG AELIN CFHOR
NAERR EGIYC SSLAE ISITY SRARL AEASU
ETRET HATRE SOANF UDHSO SOUMW NECRS
ROEUL ANHAB PTAYI OTEHE SBICR AERNE
IYLLD BSGAN LHART EGTES LTITT IYUIN
TEATB SEHIS RNUPE KTATH YEORM WKNTI
ESPOD RRETE THYOL AUTSO LMLIO IODNW
OTFEN HNRRO CTKWE OHSIL RGESE GSAIV
RYGIH UNLGT MCPAE ONEYS OPYEO LEMST
PEBUG EYKIN OTNAH DTIET OSNET MYITO
UENDT FSHSE OPHEE TLUPR RATHV IEPLI
FSTHA OOESE IECAU RNMSH YTENS BRRON
ENRHE DAUND DANEI NFDAR DUEAG SLOIN
HOERE TWSIS WOILV ULYHA SLTAE OLELR
CPTFM ERSOM DNECH YEANT WRORG DKAIN
TNRUN DSATI EARIS MCGAN HFOMT WYOOU
AODVA KAONT AEYGA MOGDH EERCY MYVON
SUOUN RLOSI EELYI RCCHR ATNWN ICSHU
'''
next_cipher_text = 'WASIRRPDYPMCTNJNERSZDVLUUSGCSPFWQMQHUVZDVLUUSGCSPFWQMQHUVRUNDMMKXTKHWOIEIYMNYCUKTTRFBROEVPLPGTUQTMCLLJWSJGVNHDHXLM'

wax_on =  'LRFKQ YUQFJ KXYQV NRTYS FRZRM ZLYGF' \
          'VEULQ FPDBH LQDQR RCRWD NXEUO QQEKL' \
          'AITGD PHCSP IJTHB SFYFV LADZP BFUDK' \
          'KLRWQ AOZMI XRPIF EFFEC LHBVF UKBYE' \
          'QFQOJ WTWOS ILEEZ TXWJL KNGBQ QMBXQ' \
          'CQPTK HHQRQ DWFCA YSSYO QCJOM WUFBD' \
          'FXUDZ HIFTA KXZVH SYBLO ETSWC RFHPX'


wax_off = 'NUFTD WHFTW HFQUU VZXCX FFTNA XMHMT' \
          'MHFHC XFFTZ AHXMT YUCXM HHAXN TFXNJ' \
          'HZTNX VATCU ZUNAH ATNTZ XDFTZ MUTUA' \
          'ZAXMH LXCNT NXACX WXMUN FVTNH OCTDH' \
          'YUCFQ UTRZH CXFFT ZATCX FFQHV MUHZD' \
          'UVZXD ATCHX YHFFT NXTRC XZMUF QUDHX' \
          'ZXCCX ZAUHJ XCHXD YUAAH MUNFT DWTVD' \
          'XZMTV ZNHZR VXRRH TXJTN AUDFH UZAHL' \
          'HFTWX XZFQU UDTYC XAAVA ATXFX CXAAU' \
          'CUFTW HFTTR ZHCXF FTZAT QXVZH ZACTM' \
          'VGHTZ ULTZM XWUZA XNUXW HTXJJ HDTFQ' \
          'UDYHU RXXRC XZMHN HZUUM TJUDX CXWOH' \
          'UZAXA XNXZX CCXGH TZUDY UDTTU JTNUZ' \
          'AHUCH DTZTM XAHDF HUZAH LHFHF QUMXZ' \
          'ZTVZH MUXMU NNXCR TWUZA TFVHR HCUCX'

class CheckIC:
    def __init__(self, text):

        self.text = text.replace(' ', '')
        self.text = ''.join(e for e in self.text if e.isalnum())
        self.text = ''.join([i for i in self.text if not i.isdigit()])
        self.text = self.text.upper()
        self.text_size = len(self.text)
        self.text_count = collections.Counter(self.text)
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.F = 0
        self.G = 0
        self.H = 0
        self.I = 0
        self.J = 0
        self.K = 0
        self.L = 0
        self.M = 0
        self.N = 0
        self.O = 0
        self.P = 0
        self.Q = 0
        self.R = 0
        self.S = 0
        self.T = 0
        self.U = 0
        self.V = 0
        self.W = 0
        self.X = 0
        self.Y = 0
        self.Z = 0



        self.unseen_alphabet = self.alphabet

        self.ic = self.run()
    def run(self):
        freqsum = 0
        for key, value in self.text_count.items():
            self.unseen_alphabet = self.unseen_alphabet.replace(key, '')
            if key is 'E':
                self.E = value/self.text_size

            elif key is 'A':
                self.A = value/self.text_size
            elif key is 'B':
                self.B = value/self.text_size
            elif key is 'C':
                self.C = value/self.text_size
            elif key is 'D':
                self.D = value/self.text_size
            elif key is 'F':
                self.F = value/self.text_size
            elif key is 'G':
                self.G = value/self.text_size
            elif key is 'H':
                self.H = value/self.text_size
            elif key is 'I':
                self.I = value/self.text_size
            elif key is 'J':
                self.J = value/self.text_size
            elif key is 'K':
                self.K = value/self.text_size
            elif key is 'L':
                self.L = value/self.text_size
            elif key is 'M':
                self.M = value/self.text_size
            elif key is 'N':
                self.N = value/self.text_size
            elif key is 'O':
                self.O = value/self.text_size
            elif key is 'P':
                self.P = value/self.text_size
            elif key is 'Q':
                self.Q = value/self.text_size
            elif key is 'R':
                self.R = value/self.text_size
            elif key is 'S':
                self.S = value/self.text_size
            elif key is 'T':
                self.T = value/self.text_size
            elif key is 'U':
                self.U = value/self.text_size
            elif key is 'V':
                self.V = value/self.text_size
            elif key is 'W':
                self.W = value/self.text_size
            elif key is 'X':
                self.X = value/self.text_size
            elif key is 'Y':
                self.Y = value/self.text_size
            elif key is 'Z':
                self.Z = value/self.text_size




        for letter in self.alphabet:

            freqsum += self.text_count[letter] * (self.text_count[letter] -1)

        self.ic = freqsum / (self.text_size*(self.text_size-1))
        return float(self.ic)


    def print_ic(self):
        print('[IC] %f' % self.ic)


checkIC = CheckIC('''
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
                  )
x = checkIC.run()
print(x)

