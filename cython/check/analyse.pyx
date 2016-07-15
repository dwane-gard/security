class WordSearch:
    def __init__(self):
        self.keys = open('sowpods.txt', 'r').readlines()
        self.keys = [x[0:-1].upper() for x in self.keys]
        self.keys = [x for x in self.keys if len(x) != 2]
        self.keys = [x for x in self.keys if len(x) != 3]
        self.len_plain_text = None

    def run(self, plain_text):
        word_list = []
        for each_key in self.keys:
            if each_key in plain_text:
                word_list.append(each_key)
        if self.len_plain_text is None:
            self.len_plain_text = len(plain_text)
        words_list_len = len(''.join(word_list))
        words_len = words_list_len/self.len_plain_text
        return words_len

    def the_check(self, plain_text):
        the_count = plain_text.count('THE')
        return the_count

class CheckIC:
    def __init__(self):
        alphabet = [x for x in'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        self.text_size = None
        self.text_changes = True
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

        self.ic = 0
    def run(self, plain_text):

        # Check if we need to do text changes on first operation, using as a case study for the rest
        if self.text_changes is True:
            original_plain_text = plain_text
            plain_text = ''.join([x for x in plain_text if x.isalpha()])
            plain_text = ''.join([x.upper() for x in plain_text])
            if original_plain_text == plain_text:
                self.text_changes = True
            else:
                self.text_changes = False

        if self.text_size is None:
            self.text_size = len(plain_text)

        self.A = plain_text.count('A')
        self.B = plain_text.count('B')
        self.C = plain_text.count('C')
        self.D = plain_text.count('D')
        self.E = plain_text.count('E')
        self.F = plain_text.count('F')
        self.G = plain_text.count('G')
        self.H = plain_text.count('H')
        self.I = plain_text.count('I')
        self.J = plain_text.count('J')
        self.K = plain_text.count('K')
        self.L = plain_text.count('L')
        self.M = plain_text.count('M')
        self.N = plain_text.count('N')
        self.O = plain_text.count('O')
        self.P = plain_text.count('P')
        self.Q = plain_text.count('Q')
        self.R = plain_text.count('R')
        self.S = plain_text.count('S')
        self.T = plain_text.count('T')
        self.U = plain_text.count('U')
        self.V = plain_text.count('V')
        self.W = plain_text.count('W')
        self.X = plain_text.count('X')
        self.Y = plain_text.count('Y')
        self.Z = plain_text.count('Z')

        letters = [self.A, self.B, self.C, self.D, self.E, self.F, self.G, self.H, self.I, self.J, self.K, self.L, self.M, self.N, self.O, self.P, self.Q, self.R, self.S, self.T, self.U, self.V, self.W, self.X, self.Y, self.Z]

        freqsum = 0
        for each_letter in letters:
            freqsum += each_letter * (each_letter - 1)

        self.ic = freqsum / (self.text_size * (self.text_size - 1))

        return float(self.ic)


class ChiSquare:
    def __init__(self, plain_text):
        alphabet = [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']

        self.plain_text = ''.join([x.upper() for x in plain_text if x.isalpha()])
        checkIC = CheckIC()
        checkIC.run(self.plain_text)
        self.ic = checkIC.ic
        if 0.073 > self.ic:
            self.ic_difference = 0.073 - self.ic
        else:
            self.ic_difference = self.ic - 0.073
        self.chi = [self.CheckLetter(getattr(checkIC, x), len(self.plain_text), x) for x in alphabet]
        self.chi_result = sum([x.result for x in self.chi])

    def output(self):
        return self.chi_result

    class CheckLetter:
        def __init__(self, letter_count, text_count, letter):
            self.letter_count = letter_count
            self.text_count = text_count
            self.letter = letter

            self.expected_frequency = 0
            self.find_expected_frequency()

            self.result = self.run()

        def run(self):

            expected_count = self.text_count*self.expected_frequency
            result = ((self.letter_count - expected_count)**2) / expected_count
            return result

        def find_expected_frequency(self):
            if self.letter == 'E':
                self.expected_frequency = 0.127
            elif self.letter == 'A':
                self.expected_frequency = 0.082
            elif self.letter == 'B':
                self.expected_frequency = 0.015
            elif self.letter == 'C':
                self.expected_frequency = 0.028
            elif self.letter == 'D':
                self.expected_frequency = 0.043
            elif self.letter == 'F':
                self.expected_frequency = 0.022
            elif self.letter == 'G':
                self.expected_frequency = 0.02
            elif self.letter == 'H':
                self.expected_frequency = 0.061
            elif self.letter == 'I':
                self.expected_frequency = 0.07
            elif self.letter == 'J':
                self.expected_frequency = 0.002
            elif self.letter == 'K':
                self.expected_frequency = 0.008
            elif self.letter == 'L':
                self.expected_frequency = 0.04
            elif self.letter == 'M':
                self.expected_frequency = 0.024
            elif self.letter == 'N':
                self.expected_frequency = 0.067
            elif self.letter == 'O':
                self.expected_frequency = 0.075
            elif self.letter == 'P':
                self.expected_frequency = 0.019
            elif self.letter == 'Q':
                self.expected_frequency = 0.001
            elif self.letter == 'R':
                self.expected_frequency = 0.06
            elif self.letter == 'S':
                self.expected_frequency = 0.063
            elif self.letter == 'T':
                self.expected_frequency = 0.091
            elif self.letter == 'U':
                self.expected_frequency = 0.028
            elif self.letter == 'V':
                self.expected_frequency = 0.01
            elif self.letter == 'W':
                self.expected_frequency = 0.024
            elif self.letter == 'X':
                self.expected_frequency = 0.002
            elif self.letter == 'Y':
                self.expected_frequency = 0.02
            elif self.letter == 'Z':
                self.expected_frequency = 0.001

class Anagram:
    '''
    Code to find anagrams in a body of text
    http://www.nerdparadise.com/forum/technology/4394/
    '''
    import os
    import pickle

    bedugging = False
    bedugging = True

    def dprint(msg):
        global bedugging
        if bedugging:
            print(msg)

    class Node:
        def __init__(self, _l, _parent=None):
            self.l = _l
            self.parent = _parent
            self.children = {}
        def __len__(self):
            return len(self.children.keys())
        def __getitem__(self, key):
            return self.children[key]
        def __contains__(self, item):
            return item in self.children
        def __setitem__(self, key, value):
            self.children[key] = value
        def __str__(self):
            return ','.join(self.children.keys())
        def stop(self):
            return '' in self.children

    def insertword(line, node):
        dprint('insert %s' % (line))
        current = node
        for char in line:
            if char not in current:
                dprint('add %s' % (char))
                nextnode = Node(char, current)
                current[char] = nextnode
            else:
                dprint('follow %s' % (char))
            current = current[char]
        dprint('terminate')
        current[''] = None

    def load_dictionary(path):
        words = Node(None)
        for line in open(path).readlines():
            insertword(line.strip(), words)
        return words

    def wordscontaining(letters, tree, word=[]):
        dprint(letters)
        dprint(word)
        dprint(tree)
        if len(letters) > 0 and len(tree) > 0 :
            dprint('keep going')
            result = []
            for letter in letters:
                if letter in tree:
                    nextletters = letters[:]
                    nextletters.remove(letter)
                    result += wordscontaining(nextletters, tree[letter], word + [letter])
            dprint('returning %s' % result)
            return result
        if len(letters) == 0 and tree.stop():
            dprint('matched %s' % (''.join(word)))
            return [''.join(word)]
        # otherwise
        dprint('cancel')
        return []

    def startup():
        global prefictionary
        treepath = "prefictionary.pyobj"
        dicpath = "english-words.80.trimmed" if not bedugging else "faketionary.txt"

        if os.path.exists(treepath) and os.path.getsize(treepath)>0:
            prefictionary = pickle.load(open(treepath, 'rb'))
        else:
            print("Generating dictionary tree...", end='')
            prefictionary = load_dictionary(dicpath)
            pickle.dump(prefictionary, open(treepath, 'wb'))
            print("done generating.")

    def findwords(text):
        withdups = wordscontaining(list(text), prefictionary)
        withoutdups = {}
        for word in withdups:
            dprint('found %s' % (word))
            withoutdups[''.join(word)] = True
        return list(withoutdups.keys())

    def main():
        try:
            while True:
                line = input('> ')
                if len(line) > 0:
                    if line[0] == '!':
                        raise EOFError()
                    for word in findwords(list(line)):
                        print(word)
        except EOFError:
            pass

    ###

    startup()
    print("Ready.")
    if bedugging:
        print(findwords(['l', 'i', 'e', 'n']))
    else:
        main()

if __name__ == '__main__':
        plain_text = '''So my story starts on what was a normal day taking calls on the front line for a large cable company. The job pays well and for the most part the people I deal with are fairly nice to talk to.
Quite often we'll get calls from seniors (especially in the morning) who have premise equipment issues such as "snow on screen" or "no signal" on their TV sets connected to our digital equipment.
Now my heart does go out to some of these folk because up until recently (past few years) we would supply straight analog cable to many homes (coax direct from wall to TV with scrolling guide). However most cities we service nowadays require our digital equipment to receive channels, and this has caused a lot of frustration with older people who don't know how to operate said equipment (ie. always having your TV set on "video" or "hdmi" to get picture). So often times we get customers who are repeat offenders with long ticket histories of these types of issues.
So anyway, I get a call from an older gentleman who's quite bitter and mean right off the bat (doesn't like that I asked for his address / telephone number to verify the account, hates that he has to speak with a machine before reaching an agent, etc.). I have some experience handling these types of customers, however this call was going to be a little different.
I spent over 45 minutes with this guy (we'll call him Mr. Smith) trying to get his TV set connected to the digital box properly so he could receive a picture. No luck. He was getting clearly frustrated by the whole ordeal and started blaming me for not being able to do my job properly, how I was useless, etc.
Whatever.
Like I said, I've dealt with this before so I tried my best not to take it personally, but eventually I had to ask him if we could book a service tech to the home (a courtesy call) to get his TV working correctly. Unfortunately, our booking calendar was showing an appointment 3 days out. That's when he dropped this on me:
"Don't bother sending a goddamn technician, because I'll be dead by then. I'm 94 and TV is the only thing I have left, are you really going to make me wait for a tech?"
I instantly felt bad. I mean, I've heard every complaint in the book as to why people don't want to wait for a tech but this one kind of got to me. I'm in my mid-20's so honestly I can't even imagine how it must feel to utter those words.
So I spoke with my supervisor, who said they'd see if we could get someone out earlier...but we couldn't promise anything. So I let Mr. Smith know and he was predictably not very happy with my answer.
At that point it almost sounded like he started to cry and went into how he has no family left, and no friends that come visit (this was after I asked if there was anyone in his building that might be able to help). Man. I felt terrible, so I took it upon myself to ask Mr. Smith if I could pay a visit (he lived in a small city over from where I was, not very far to drive).
He was a little shocked I was willing to do this, but sounded thankful I was willing to come out and help him personally.
So I head over, get to the residence and meet him - within 30 seconds I had the cable running again (simple input change) and even brought him a simplified remote for his set top box to avoid this problem in the future.
That's when he started crying. He goes into how he hasn't actually spoken or really interacted with anyone for years. He gave me a hug and told me how thankful he was that I came out and helped him, and told me how sorry he was for being so mean earlier on. I said it was no problem and I was happy to help, and that was it - I left.
3 weeks later, my supervisor comes to my desk and asks me if I could come speak with her for a bit about an account for "Mr. Smith". Turns out, he sent the cable company a letter outlining how thankful he was for helping him with his issue and how it really "made an old man happy again for once in a very long time". The letter was framed and put on our front entrance to retail.
I guess the moral of this story is no matter how nasty someone is to you over the phone, sometimes they're not always a terrible person and just going through a lot. I still think about Mr. Smith occasionally when I get those nasty customers and it makes me feel a little better.
Anyway thanks for reading just thought I'd share how this one call changed my outlook on life :)'''
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
        plain_text = ''.join([x for x in plain_text if x.isalpha()])
        cipher_text = ''.join([x for x in cipher_text if x.isalpha()])
        chiSquare = ChiSquare(plain_text)
        print(chiSquare.ic)
        print(chiSquare.ic_difference)