import itertools
import multiprocessing
import time
from termcolor import colored

from pad.pad import Decode
from check.analyse import CheckIC, ChiSquare, WordSearch, Dia


class NthMessage:
    def __init__(self, nth_cypher_Text):

        self.cypher_text = nth_cypher_Text
        self.plain_texts = []
        Decoder = Decode(self.cypher_text)

        # For each shift posibility decode
        for each_letter in [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']:
            self.plain_texts.append(self.EachMessage(each_letter, Decoder))

        # sort each part by its chi of the english language
        self.plain_texts.sort(key=lambda x: x.chi)
    class EachMessage:
        def __init__(self, shift, Decoder):
            self.shift = shift

            # run a Vigenere decrypter
            self.plain_text = Decoder.runner(self.shift)

            # run a beufort decrypter
            # self.plain_text = Decoder.beaufort_decrypt(self.shift)

            self.chiSquare = ChiSquare(self.plain_text)
            self.chi = self.chiSquare.chi_result
            self.ic = self.chiSquare.ic


class Run:
    def __init__(self, key_len, cipher_text):
        self.key_len = key_len
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z']

        self.cipher_text = cipher_text
        #self.brute = itertools.product(self.alphabet, repeat=key_len)
        # self.brute = [self.pre_analysis(), ]
        self.decoder = Decode(self.cipher_text)
        self.pre_analysis()
        self.transDecode = None

    def pre_analysis(self):
        # Build the de-shifted text that is the best gueess from chi-squares
        messages = []
        j = 0
        while j < self.key_len:
            i = j
            nth_cypher_text = ''
            while i < len(self.cipher_text):
                nth_cypher_text += self.cipher_text[i]
                i += self.key_len
            messages.append(NthMessage(nth_cypher_text))
            j += 1

        return messages
        # Build the key from the analysis
        # w = 0
        # while w < self.key_len:
        #     key += messages[w].plain_texts[0].shift
        #     w += 1
        #
        # return key

        # j = 0
        # for each in itertools.product(range(0, 1, 1), repeat=self.key_len):
        #     key = ''
        #     for each_char in list(itertools.cycle(each)):
        #         if each_char is None:
        #             key += '.'
        #         else:
        #             key += messages[j].plain_texts[each_char].shift
        #             j += 1
        #     yield key



    def start_combination(self):
        ''' combination cipher '''
        pre_analysis = self.pre_analysis()

        # build a generator of possible keys
        for each in itertools.product([0,1], repeat=self.key_len):
            j = 0
            key = ''
            for each_char in each:
                if each_char is None:
                    key += '.'
                else:
                    key += pre_analysis[j].plain_texts[each_char].shift
                    j += 1

            # using each key test it
            each_key = key
            print(each_key)
            plain_text, key = self.decoder.runner(each_key)
            chiSquare = ChiSquare(plain_text)
            ic = chiSquare.ic
            print('[-] IC: %s' % str(ic))
            print('[-] CHI: %s' % str(chiSquare.chi_result))
            if chiSquare.chi_result < 100:
                print(key)
                print('[+] Found a possible key running diagram analysis')

                # test the resulting plain text as a transposition cipher
                self.transDecode = Decode(plain_text)
                for each_degree in range(2, 50):
                    # print('[-] Running %d degree' % each_degree)
                    dia = Dia(plain_text, each_degree)
                    dia.permutation()
                    dia.run()
                    if dia.key is not None:
                        print(dia.key)
                        trans_plain_text, trans_key = self.transDecode.permutation(dia.key)

                        # Look For words
                        wordSearch = WordSearch()
                        words_len = wordSearch.run(trans_plain_text)
                        print(key)
                        print(trans_plain_text)
                        print(words_len)
                        if words_len > 1:
                            print(words_len)
                            with open('combination_cipher_result.txt', 'a') as results_file:
                                results_file.write('%s | %s | %s' % (str(key), str(plain_text), str(words_len)))

                        ''' Single Thread '''
                        # for each_trans_key in transpostional_keys:
                        #     plain_text, each_trans_key = self.transDecode.permutation(each_trans_key)
                        #
                        #     wordSearch = WordSearch()
                        #     words_len = wordSearch.run(plain_text)
                        #     print(key)
                        #     print(plain_text)
                        #     print(words_len)


                        ''' Multi Thread '''
                        # q = multiprocessing.Queue(maxsize=50)
                        # jobs = []
                        #
                        # # Create workers
                        # for i in range(0, multiprocessing.cpu_count(), 1):
                        #     p = multiprocessing.Process(target=self.combination_cipher_worker, args=(q,))
                        #     p.start()
                        #     jobs.append(p)
                        #
                        # # Feed items into the queue
                        # for each_item in transpostional_keys:
                        #     q.put(each_item)
                        #
                        # # Wait for each worker to finish before continueing
                        # for each_job in jobs:
                        #     each_job.join()

    def combination_cipher_worker(self, q):
        while True:
            if q.empty():
                time.sleep(1)
            try:
                obj = q.get(timeout=1)
                plain_text, key = self.transDecode.permutation(obj)

                wordSearch = WordSearch()
                words_len = wordSearch.run(plain_text)
                print(key)
                print(words_len)
                if words_len > 1:
                    print(words_len)
                    with open('combination_cipher_result.txt', 'a') as results_file:
                        results_file.write('%s | %s | %s' % (str(key), str(plain_text), str(words_len)))
            except:
                # print('[!] run finished')
                break
        # print('ending worker')
        return


    def start_simple_substitution(self):
        ''' MultiCore '''
        q = multiprocessing.Queue(maxsize=50)
        jobs = []

        # Create workers
        for i in range(0, multiprocessing.cpu_count(), 1):
            p = multiprocessing.Process(target=self.worker, args=(q,))
            p.start()
            jobs.append(p)

        # Feed items into the queue
        for each_item in self.brute:
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
                plain_text, key = self.decoder.runner(obj)
                # plain_text, key = self.decoder.beaufort_decrypt(obj)

                chiSquare = ChiSquare(plain_text)
                chi = chiSquare.output()
                ic = chiSquare.ic
                print('%s | %s | %s' % (str(key), str(ic), str(chi)))

                if ic > 0.06:
                    print(ic)
                    print(plain_text)
                    with open('vigenere.txt', 'a') as results_file:
                        results_file.write('%s | %s | %s | %s' % (str(key), str(plain_text), str(ic), str(chi)))
            except:
                # print('[!] run finished')
                break
        # print('ending worker')
        return

if __name__ == '__main__':
    # key = aaabbbcccabcabcabc
    test_cipher_text = '''SOMZTUQTASUCRUUOOYHATXBTCPQRNCLECYUCKINHDBNNUOOVHFHRPPTLIOFGQTCLBTGFEACNECONQBPAVHFLOCRAZUWELMBOF
    HQRUJENQSURARTUIFRGQPMGIEGAMYITHBSFHCKRMANJEEUQTALLUPSWKTFQFUGNXGLLGFUDCNNSGTONUEOKORSFTQGEKAMNYJPTIGMOROJOIYJOICVFRRF
    OISEFRVKROEOVITUUFUSUCIBTUPQWPPSDTEFPORNPTJIPCLPPTIGISVVSEUTDQPPEDVEEVOPWRDIHJUCNGQVKPNGNUPOWMZIFCTVDPGSHQOVVTOSPNFQHV
    HFUEGQLLDECAVTFWRWNUKLSGCFPTLYQBTVHGWZGASUWFYOULETVRRNYTVRBKGIVANAMPHECDLFVONCNZJOMETDPCZFISGCUHRPOWALMUPVXYIUJSDTOMNI
    NGHVJFGJOXGVFTMPUTCIUJFUYGSFTVJEEOQWADBZTTGSUJTEPWREKGITBMFSWKPNGNUVOSGCEIWFDJCPNFNSBPDUJISHBTDCWUEECLPVOGHRUSUSBVKQNX
    KTIQLEGRPEPQMGYJOEQNUMNPYHOWUPPRGTAUGSBKDFSUIPNFOVKGAMYAZUHBXINGZPVTVXSFVOOXIEGOORIENKVQGFVPJETVTESOPGUGPVINGSXGGFVCUSU
    PNGTUWIQASGRFREATPGGGPFESUWJVHMQNGTJDLGVJITVOSKETQFTHFTFVARETQFJUSVGSSOBOZYCAIHGTBEAMNFRONBOQNFESIEOVLFOANWIPTSWKTFDIU
    VESCNDMFBOTKIHUQFGVHFDATDPFTPVNILGTICTJCSKEEGPTJKSBFDSGSTVELEQIPPGPUNDESVOWGRIFZUIGCECPWNUJAUGSTHBUIGJCSUQSQGALYITHBNBE
    JKNFDEGQRFTEACIJOICPAHGNUGTDKHAVFTPOGGXQGRJGNDGHANEMJPIVHFUEUAPFUOFCVTUQOGRTJOXGVFTTHITDBNNYATIOJPGUQBEAMJUVNGDJHFFTEO
    VISPFOUQXGRNKNVVETYITHUIJUIWYXGLMEAMNHIMNSTOKVHUTYJPGUQGETIJTVXUEUEOOPEDVEDTPUIGFKGJVAMDOYRROPFSMAUQHFEOVNDSGCEIWFBRKET
    VTEOQLVEKHEXBTIGVTJPGDNEBTLYFSVTVTCTFFBZVHFYHOLFPSFGCLBPDTVASVEDBMBNKPIMFHOSPOUDEINHBCNGVOEQMZLOCRROPFSMAJQWJYATWSFNES
    SFUDYJCTFXESNILGISAJEJXGFEBNTXKTIVHISCFGQTGSPKTSKEEOYBETUOQVVOUCKFKTQGRSOOBMNADUUGVFPTVCLLYJIBFVQATMHJOIGYECOVMEDQQKBU
    ESXIDGTECIUPVJGHPOEBEOVTTESZDBNNVOHGTIKSUXWORLJOIEQRSGCUNYVPFORUVOCVGLZQUSDOPMINGDBMGPFASYATUHPYINGBOBRRQIOVMFPTECYSOV
    UUJCVSXJEOJEETOPPFEUJKUOOOEEQNUDOTHFSTGPFIOIAHQDECMNTFDIPKEIBPBFEAVUEILMCFFGCDCATIGNJOANDUWJUVJEPPLZVHJPGIHBWFNGHTBTEZQ
    USGALLZHPKPITPOALGMFYAITGPSCVGCIKIOUTBPTLYGFMVDCDJOEBPIWGHEASEFXGTYDQMQNAJPTINUIFDQQKBUTPYHZREOPMFEQPVWBPTUQWBKTFOSBUGE
    JBVVTIKSPPEKIOEPHIQTUQMFKMJPMYMJETUQJOOGSUNYJEANTFWFPKOAHKNFJOXKTMUTUGGGNTPWTUGRUJOSEXPSFUUOJUPPMEXKTHMZTVRGTVJUOSYHPUA
    IDUIFAFUEFKFXGCPWLDGFUTQOGOOGOVVEBTLIESCVVYGCPWLEPTQTOMITFBPAVHJPGTQIMGTMRTNJVJMNPYAOFHFYASPSFEKEVACNYOQTWGRYHBQQAYKTIO
    YBPSXGRATUIBVRQIOVIUCLNQSTSPVOFGFLJMEIGSUCRTEEUPETAAOFWFPTJPTOHPXIGJCSOQFBOIMALEFUBOFPQFSKEOFSUJATCPNFXKUIUVHJUWBUAFTFS
    JCUMEEKFUJESGWASBOZQPGIOJITDUJNDINHUICVOIHJTCGACNETOIFMROCNJHEMVTFTRIBMFTQKVOPMIUWPPPMYSFMGVQCSLORTOIUJIFIDPVNFRAZCVJUI
    UJELIWFEKPCSNCLMEIUAOVESGSQOYHFTEJYATPOTVFSZHCTTPFRJXEIGWASBMJVVNETJODMEEKWASXJMNKPGUQDPVHJUBUTTPVPFGDUJAOMFVNIWATXJNNK
    NHVODQMFQUTAOEIGNRHJOPFTSPPALLZTPKJGAEQVFTGFVTOTIFSGUKDFPCFCNEOEETIJNYKVHJPSFEOOFSIHBEUJGEACNESWNOKNGAHBJPUKMQNEJPPVVCH
    AOHFCPFEWGNCTOVIHTHJNBUKOPMKFJGDSGMOTFGPTJKSTGTUQPCQXTOBWPKFVHJUPSQBMGMINUIFHWVUSGTICTTYHENIFTVCTTFFCSAIOIHEGPFTKPVOIQW
    IGHBUNTADUVCNNYTROLGNPTREAMMZKPVESCCUGDXKTHAOZPPGHOSAEBTSIGGAVFNFCJWGBPDUQLEOEHOXUICPMFVNHFYATVHATJDBOGQUUCNEJEMREDHJNB
    PFVOMFMFJOXUORRZIFYCUFPTBFKNHUOMEBOFCTNIFTOOKSBKDITXBTPQRRPDLFOAOFIWATIBRRATPJEMRAOFTHAUXBUKVIMGFUYEFMSLAUFSOAUUQGRWKS
    PTCOMFTUQOADFUKBPDBUKSMFJGKEQUMFCPOETREAKXJUJJGRGQRBDIUCBOUUBOCEEOVPTGQRNTSMIUIUWTPSPWTIGSFPTTHFDBDNGCPOPBPYBNETTFSPWVN
    IOKNHJOXVHANLGVNJGWBUFPTHFNPINHIJOYKTIJITKSTWEANEIPYKVRFCLMAMBFEANPMEOCPHBRPZCGBKNFOSPOEGKNBXESALPPGTINFUJGNEUVESYATHRA
    MFEBPFRUUQNPWRGTONTFOUTCPCFVOSGTBKLIGVFTUVJENQRBNOGVHISTUPTAKSOQMBVTFTHOWOBTVAUONGOOGITVOYOVPWGTVHFRHPPETQMETJNFUVJEZTE
    OQTBNWAYTBUGTTICNEQGRTQNANEKVUVIOJPGUJRPWGHAMPUKUVIMNTIKNLCBOUUNSUOKTIQCDCSJQNALMZXJGPIHGTUJOTGNASUZDWUVONGRTCNEKTMALFT
    OGHEFNAMKTUNEBEUUFTCPYXCYUJAOMSFOSSFCFKNHLUTVTIQUGHUJEUJCRFJOXVHJUONEDBMNEJAOIEEOYPWTLOPLPPNKFF'''
    test_cipher_text = ''.join([x for x in test_cipher_text if x.isalpha()])

    cipher_text = open('cipher_3_text.txt', 'r').read()
    cipher_text = ''.join([x for x in cipher_text if x.isalpha()])
    combination_test_text = ''.join([x for x in '''
    VWXJGVXCJGHXCEGUSHSODXLDOVRCXOKPLJHRETYUHGWWGUSESSYJZYHPPYPTYSLWONVPNOSFPNCWQLYMOXPUCWFLJG
    LAWWOKRQZFOXPXCAWALFAXSPDVIAWSKMPLZPAESOLVQLWSVJYWLGEZHSEVECBUTESMSEPBLAWWUAINLZZPQCCZQPYW
    YSDPGLTNTOSPJTBOXPXCUVTYUOAZSOLZACSPQDPSBUTAAUIETGBWPDGJYSLGUWZHCZRNCSUIZCBZSTRBSEZYHLLTCH
    ZZPEGVGYYSAGPOHVSFCRNMTEOLPBFWTTPYHVRHXMLLLCHVHPDUVSFEHZSZXSMSESSLWQZZIOPNOZYPFDUYETZLVNPB
    SXJAOAWQPKLCLCGLAHZIKPDFDSTJDHHVTRVHXYLZNSNLPLPEZAUEJSCLQDNCEEOTFJIEQFTSHLZAPZEJPAESGYGZWZ
    UMRRIKMPSCLAGPFVQDEQAMTPGLADPFPZNPBDSLOOZCCPEPYCPCYYOTUAMLWSBUTAAUIEECLVNPWLZNSOURPWGUEOEV
    ZMSLGHGFDSHHWZHMSQCIAWCLHVMYHWOXZWRYIAPCSTPHVKSZYHUOZHVDSEZCLTCLHZILTRXIFTDLQYEWHIWHOZCSLJ
    UMRJCYYEGGAIZYJKMPZCOVOXWVXRPHPTNEILVDZCAJPYHTMPDKNIPEQZYEZAYIDHVHSCPFWIPLHMSQPBLHCDKAMSWC
    NRETQLOESWAWZCWZIZQHLLDPHWCPDCPJDDIZIDZOFRHLMNMPEOHGWWTVVXLBSSOPFLKYEZTILYKVLDBIAMPMWAXPCO
    KRXPOYRTRVVXQQHLLMLHVHPDBSXTVSOXLEWZEVPRVJCSWHWOOFZIDESLPASCLRYFALFCECLZCTTACSPOJGZFBOXLES
    AWSLHLLSLGVXDASREHTHHLXLQPLYPPMIZCSLVLNVUMRLBNEPYHAINTVCEPDCLQPIDYITPBLGSLBSHTYUOXPDSFXAPG
    MSNFGVXXPFOWZHSLZCEVZMNLZDPLDUPSYRHISPLZAMEWSPHQQSLVYEWWWPYHCSPCAUMFESDWTEVOXTDUFYHPZJPLWZ
    PLXXFTWTEVYXJTBAKZRSOXTDHZZPEQUSYPQLXOECOXPOWPKELZVFIAFWSPCZZCZSSVGFWRLVNPWLZLAWAGFCSVRWFQ
    OOPHONWPEHUMRNZHICWMYJFDHHVEPRFFESSOAZWSYSOPOHPYOGHXCESIHWLAUMRXSVJCYCIXPTBHKMWSVXOZAQCZMD
    VVAPFFPSZKDMLDILWWPGLWENKHLEPJYIWTYPIDLWPHGPRHIWEKAMSEVZMMPTYSPDCAMCTSTHJMSAWYZHVXELYPIEAS
    ZVZYOSPJMILXGPBBXLWZPCSLRVXLDYPLXTTLANZIKPMZCHODPFPZNPHJISECOXPSCLQLNCYYEPGJCLWZVXRPHPLDEJ
    VACVWNRNZFLVNEZBCYQCAVFYOLXWJCYYMZCPOYRQSEPYRYEHLGOWZHWNRLYOWTZTBTXPYHHHJDCAYESOZXHSSORPOF
    WSAPROXTDCTRPOCARMZHLLCDSKRTYUNEZORTEYESOGYTQHMYMSHGFDSSMWMSLHLOPACSPBTMLYRCXTDHLLZYZACSTB
    PKSLJSIPQHYEPJCYYPLZFPRZWNREZAREPXSHATETYSLESOGTTBAWLYHFPQPZIXLOWLQLYWLZSPOKVPGSFVNZASTLTB
    PXYEVIIZZYZEEZKFLAPCSTPOCARHLBAXZHOAMQZFAEPNVBFEEVZMZYSPOYOCNJZEHTSPTAUMXJAKMDDCVLYPGSXJTQ
    UEEPJUITXOPKYPVDSTEAZYEQSSIEZIAXPCHVLDPKYSODGPSDACLOHTHTLJDILTCGWVWCHVZSLTROXPJRLWPTTLANZI
    KPRPHVWXPCLRZFHHICWWYIMFHLANZIKPYEDVVXTGHIYJHPLYRGPSWPHYQDXWOXVYCHAYOVDILDDLVOTQHXMWMVREGS
    FVSLDFTHTHTLJLBDWPCOAXSLHVTTYHAMLWAZSEDCUYOPRPPVPVZIELFLXOECYGJLBDHPYHUMEZVDSSPVZEYZTTETWM
    LPQEOKRYZTPVPYRAWSLHVGXPJZMTEHPLDHOHWQESPVLDYKITQHLLCPKZELYMUSPTBPLDMISMOTBAKSLHPQRSHLFLMZ
    AIZSSWPXLBMMPWHLXCCWSFPDCAMZZYAMFACTRJDSMPEZORWXCGPQESWPJNZIKPALMCETDWOXPWWLZOTBZEXLZJPTEM
    CSPCTVVXHVYIPTKZEYZHLZCJTYEEZRPVGPVDILDOPPEEZZISZQLOOTKZEHTZPPYRHKSZEVZMMFHVWFYRKIESORRQFZ
    DMLDKSMWTBAKZNCLQZFHUEOSSWPSTALTCDCHRWWMVWTSSKEZGSNVPEHASSPFZITOSJRPLBTHPPHPLXHWOXTYGJIZYR
    PWSLROXPNOSFPCIURTYUNELTBPWXAZPIYAIJXSLBLKLYRCIPYPVVFRVOXTXOPWXAZMMTPRLVXZHMIZCVZMDPHVXAMC
    ABZLJPSOEVZMACCSFPXWARSPTAYFCSOXLEGOAPYVZIELFLXONFPCYRVNIZPGUMEZVDSSPVZEYEOAGFLZFPDACLOYZF
    LVLWZPCYESHVNESDHTEVUEJZBMIZCMHICDVNILGSLQLSIHKYOHSSOXSVLHEVUEVQIOPPHOAWSLHJMLXSBSELBOHPWD
    KISTAUEOECKPXPVDSDZFFVSPKZEQZFLFTYUVWXPOLRLCZLMCZBZMLTRAMHLGVRACCSFPXOKRTHOOWLADACZSSWPLYR
    OXLEKZETEWLPQEKLIVDZAEPCAZCFASCVTDCJVZXSAWZXMLHDVOKRLDYTWPTTJMZFZJHZXSWWPLYPAESVYIQZFIETEO
    VFFEOHRNNCUYEQCTVCDAAMSEIUVDZIOXPDSARESSHGMWSVGXAOFRLWSAXPCCAYWTBUMRSCAASLBMOFWVDILDTYSSPZ
    PTYRVTMHTHOLTDWZWFPOKRSZKAMCPOSPJXOLHLYCKPXLBHLAAMNELTBVJCZBLGTYOLZCJZUSREWLQESSLPEESDVLDT
    HVXPRUEOAIVXYZIMVCZBLXYEFUENPHYSPEOSMTRIZIDEVTIZCOVPQEVZMDECFVTDBTSLEHYISZKHRDEMVWXPCLRTDH
    FSZFCLZCEVWISZBZIZXSPXXPGOXPJFUIZEODPLJGAEPCFIMWPDYIDZBUEOUIAWRZWNRESFBSRSOVPETGPXWWHPLYVO
    VFFEAZVXTHVLNNOPWZYOSPJHVUITRSAXSZGUILDHJCFDHTSPCGUEOTHHQVPGLQQPSHPWTHSXPMSAXPCOFRHLMOXLYY
    MWZCFHIOTBQKFDHOXZFUALTOGHLCPVDSESWVWYPQSEWNVUERPRFQZFHVPZVCSRTQS
    ''' if x.isalpha()])


    for each in range(9,900,9):
        print('Poly-alphabetic Key length: %s' % each)
        run = Run(each, cipher_text)
        # run.start_simple_substitution()
        run.start_combination()
