from co_incidence_index import CheckIC
from corpus_analysis import Analyse
from brute_force_vigenere import decode


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


def ze_shift(cipher_text):
    cracker = decode(cipher_text, 0)
    cracker.start()
    return

def ze_analyse():
    checkIC = CheckIC(cipher_text)
    checkIC.run()

    print(checkIC.ic)

    # Print IC of all the letters
    attrs = vars(checkIC)
    print('\nletter frequency')
    print(', '.join("%s: %s" % item for item in attrs.items() if len(item[0]) == 1))

    print('\nletters not used in cipher')
    print(', '.join("%s: %s" % item for item in attrs.items() if len(item[0]) == 0))

    print('corpus anlysis')
    analyse = Analyse(cipher_text)
    analyse.run()
    analyse.output()
    # count = 0
    # for each in analyse.bigrams:
    #     if each.frequency > 5:
    #         print(each.name)
    #         print(each.known_frequency)
    #         print(each.frequency_per)
    #         count += 1
    # print(count)

def ze_test():
    # test = decode('TIKSJUGPKNHVOCGAWGRZGVFPTGWLFXEOKNH', 0)
    test = decode('IXCSX QRLKN HCTBU TBTTV RTFNC PYHPY ATIEU VIOII OVOFV HFTNF VTBKL TCNEK XXGPV VERWI QOEOV IOCLP VOGTD QCRUA DBVAD GNUTE TCSUJ EZYES GTIGB FUTQN ADGTP EOOPE DVWJV HJUPT CNEQT IGRDC RSKES UTIKS QCRUK CVNAS FAUCC FPTSG WBUOO GOGVH FQLEG RPPET JAEDE FPFVN LGQRZ GASUA OFTIG CPOPB PYUJA UQPFT AUGDJ VHBFL PPGTK NDGFP EUTGD UJEJT AUVEO VIPPO OVHFK ROGWF TSIKN JGREC TBEEO VRFVH BVIUY ATCCU WAMNY QQSTK BMGTP UTJNL CWYTR ADGIO QNFIU ZYHPK LMEAM NDJEK XCSSG SQQNT KBMGF PTBPV HBPDE KDOVG JXEBE RBRAC QUUVH FQLEQ NFUIO EEUJE SGWBU NPUTS WCUWR FFCBD LJPGB PDJVW BUINR OTUIC NEUQG FVAOA OOGOV VTPKN TVAMN AOAPF QPMGJ VUTSC NUJEJ TOXPC BDLJP GVPDF TTIGF MQOSC NEVHF TEXGR FPOSG CPTDT CSUQW IGRFC NZQFJ VWFPT JFVJU IUGDU JESQO NVOJP SUCLM CSXKT DJWIG NJPOU KCFFT ICTUJ EBKRD QNEKT JQNFT WIKCI YATTI HJTOG XUVOP WRSCC LJAEV WPTEE NIHJT TQNJV SEKSQ NAZRA OGLNK NPTAM CRNZM BLOSC LBTMY EOOEE SPEEK PJEKF FUQVH FRHPP EDJHP RSLAH FADJE KJVHJ PKUJE SGSBR RPDLF OWJVH UJEBE DPYNI GRFKT TIOUC CPWPM GOGRR FVTZU ESKOV ULPQK JPGBN ASOLJ IHUUO OKTBP DUJES QONKS BNIUV LFYAS OESVH BPNPT MBNYP WSIQU MFPSQ BBDLZ EHFEK JVOVV DJEKP JOLCY UJAOM SGQRM GTUKN HOELP OXKLM NOPMI OVOJV TIKSX CSIKS VUUBN RFUPP PSFYH JEHXC SGQLM QWFFU QDYIK SVUUB NFPNL PYUQY HJEHX CSUQD PCBTQ LVVEM ANPVH JPGUY OXGEL ULBVE SKWFP TCCCL VOEQS POEQC TDJIO IAOFN PVIDG DUJEM KGIVS XGRFU TJNLP PCIJO QUKZJ EZVHF UEBNA SOLJI HUUAS GOOCG BKNKW SUVHP WGIVY PWSIQ UMFKO QWXJA UGVFT YPWFJ ZEEOU TVNUJ AWGTB MEOFI DMOIQ KBATI CNLUF PTLFV TJPGN GKOQW JNLMQ OLKNU QIUKS JIHFF AOFWB NKFFB BEKUQ TIGOG HIDGA CQUUC MPPTI NAUGR JYATU IUVIO IAUOY EGSLE ATWAM NYQGR VUIOI TIGGS CPIKN HUYTV ENYHF PIOQT JEEEV HBVPF GRJPG UTAGH IDYAT FRPRP JPGPH FOQTT NOXNY CWTPP ECKGD JUOMA UCTJO EHGTU KNHNO XGRBP DMQWF TEWGR ZHEXO IOWTF UISCC FFTPH IOFOV VWIGT IGRXG HBFAH TAQJI OIPSQ BMGMC WTRWI DMLZP OUKCF FTICT GQRFX ESADS QPPHF JPTSC FGKCU JESQU UGRXC SSGPP TTJPG PPEMG STREF TPFGR TYESG DSQPQ KNHQF GVHFP EUYOS MBVVH PYIPU BVIMF OOSAL FCKUJ EOKTI KTNGA MNOGV HFREF TSETO QRIOI OGHWF TEJPT ICTEE AOFTI GYXGR FFRPR PJPGP HFJPO SFESQ FQTOY KMJVY UQOVT RBEKJ EAMNE EFIDM BVVHJ UPIQN FFIEP TFXEO TIOIA OFIUF IEPTH QTPXO JEENC IMLUT VFBKL FFISC NPWTP HTIGO GHIDG AOFSQ TIOVE EQFGF OXPTI GSUTE FVTPV HFFCV ROODU TVIOI TITOV IHUJE EQOSK HFCRE CVFTY XGISF SPWNE WPPPT BMIOI MZHIS UTTVE QKTXC SNQSU FEGKN JVEMA ATRLB UHJNO PMEEF OXPAO FIXCS TVAOF IOIIO CNJPC IQFXC TFTAC QVFCR BKSFF FMQOS EMEGE QHIMN EEYIU JCBDL FUDJT EDVLZ PEYVT PVHFD AUVES ABBPK PHTIG UQUWI KCIYA TQPFP WJVHF ZPPUE EYISK NHJEB TTKWM QGDJP TPOYN QUUJP PWNEK NHNIL GAKCC LJANO ESKMB DOVVT PFIFD UUKDJ FNUCN EKVFT YTNOX NYBPD DCRFH UMNYU QOLCS UGPCC CLQNU QDSAG SQUOF LPQKJ PGVRT PVHFG NEQFU JESQW JUAXV WPVRB FETOE OYIUJ SPOEG NOPTT JNETW PBRUN RAOFA MCRHG DSAES EHIQP TMYXJ AUVHF JEMNH BRPFP EEYHF TEJUD JEKBP DXJYJ UNUJI TRHPP EXQRL KNHVR BFIFQ HBDOV VTITE FAEBT SBIOE WRJPG UJEZG ASNYT GRWKC FKNPV IDGDU JAUVH FRLVI CBROO VHFJI HJPSG STWRF EHJNL FFWBV ESNOP RHBFD FXEMQ PFFAD TADMA OFWBU FBKLJ PGJVO MFDJE KBDOV VIUCT UJEUK MFCNE JETCI EJEEN OPMIO VOJVI HWETU HFFIE PTCGC BWSFK TXCST VIMNL JMEUJ ITVHF NATVT XQYFC RTYED CMFKN UQSFT VJEEJ VTIKS NQROK NHCNE KTBRP FFIUV OTGEJ HIUYA TQNUK GIVLZ NOOIS UQRZU HPTTJ VLJVE SCLMA EYRLP FEEPO XVHJU BVKLE KNHYA TCBPW TTVOS KETJI HJAOF WFYES GOONE WGLUJ EDJIM NESUF PTTIG AJTCP PDJVI PPESU WFTEP PTIGR PQFTQ BZVHF VINGT IGWBV ESKSP PLFXE MKTTT EBNLZ JIHJP SGSTW RFYHF PTIGC BRRVR TVTEE YAUGR DCMFQ UUUOI CRECN EHATV TICTJ VSIQT UJEDQ NDTEU GFMQO SVIMG WFKGI KNHMG BVLFC SUWPP HFUJE GNOPT AOFKJ EKFFI UWPUQ AEGGS GEBPG MGTVT NJPGU JETKN HNECN ATVOG YAUGR JPTPC HJIHQ TETUU SGSQT IOMLF TWIKC INICG RBNLZ FOVUE EVHFH ISUTU JRFGR BEKTY IUJWB VESVH FHISU TUJRF GRBEK TEOOV AJPEE VHFRR JOASA AOFBB EKVRC PTEWQ IDGSX KTDJE THOSV HFEON RAOAF PTTIG EOVIS GSUCT FAEQK CPWLE PTDCL MFIDM BFEAV UEBNL NQBJN ETGRW KCFUA OFMPU TGKXF FLJPE TGRWK CFUFP TTICT DCRSK ESYES GDPYN UJETW BGNOP TSMQW MAFJN LFFUQ YIUJW BVESV ALKNH QUUTA DMSPP ECAOO GATKT IKTUJ EJTPP YESEO OPEDV IPPSB NLUJE DQPQG RDCBM KNHWN EGRUJ EGNOP TWBUR VKNFF HVPDS GDTKF OQTUJ OVUAO FSPHI OVEST ADMPB VCIGS BNLEG AEVHB PKGWL MAIUJ AEUTP RPFFC NUHZQ FTRIM NIOIO WGRJP TPVHF WPTDA UVESA BBPKX JIDJW PWLEJ AWGKJ NLFFM FKNTV AOVLZ DYTJE FTLVE KQTEQ CRBVI PPOVT RBEKX CSTCF FYEXG RFVHF OOTVU QJIMN OOVHF UUCHL PQRBP DJJAE OAEGS VTEUJ AUYHF POVTP PYESY ATKNT VAMNE EVHBV IHQTB CSDTE XKNXC TFTPS QOGEO OPEDV OSCNE CLUJO VIHJV WBUWF VWFYE SGVFT YNWCI UTJNL PRESC TJPGB PDTVI MNOON IOGTI GDDKS OQLPP GFTOQ GRBVI OIATC RERAS VYSQO NCNEN IUGRB NLZGV FTYDW SUQMF THBUM PXEEQ UUPEY VTJOE JEAMN EEKNT QMFQN FGLTG AOUWF TEEFI DMSQJ OOGAO FIOVR PFUDG DIKMT GLGCS UJEOG WGCCJ NIUAM BPAHG RJVOM FHJOI OGEEG DUQGF VSPOE GKBSG PBVCI KNHKN TVAMN EEVOB POUJE SHLPQ RPHTI GBVKL EKNHC NEVHB VIEUT BTTFF TIGPS QCFUS XKTIF IDMBV VDJFN UIEUC RFUPP PSFVO NALBU TFOAJ NNFYD JEKPJ OLCYU JAOMS GQRMG TUKNH OELPO XKLMN OPMIO VOJV', 0)
    print('here')
    test.start()
    print('here')

ze_shift(cipher_text)
# ze_shift('DFUPAHDFUPEHRQS')



