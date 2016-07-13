import itertools
import multiprocessing
import time

from pad.pad import Decode
from check.analyse import CheckIC, ChiSquare

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

            self.chi = ChiSquare(self.plain_text).chi_result


class Run:
    def __init__(self, key_len, cipher_text):
        self.key_len = key_len
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z']

        self.cipher_text = cipher_text
        self.brute = itertools.product(self.alphabet, repeat=key_len)
        self.decoder = Decode(self.cipher_text)
        self.pre_analysis()

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

        # Build the key from the analysis
        key = ''
        w = 0
        for each_char in list(itertools.repeat(0, self.key_len)):
            if each_char is None:
                key += '.'
            else:
                key += messages[w].plain_texts[each_char].shift
            w += 1

        # flip the key, it is flipped later in the decrpyter for important reasons
        key = key[::-1]
        return key

    def start_single_core(self):
        ''' Single Core '''
        self.brute = [self.pre_analysis(),]

        for each_key in self.brute:

            plain_text, key = self.decoder.runner(each_key)
            chiSquare = ChiSquare(plain_text)
            ic = chiSquare.ic
            print('_' * 10)
            print(ic)
            print(self.key_len)
            print(plain_text)
            # print('%s | %s | %s' % (str(plain_text), str(chiSquare.output()), str(ic)))
            if ic < 0.065:
                # print(plain_text)
                with open('running_results.txt', 'a') as results_file:
                    results_file.write('%s | %s | %s' % (str(key), str(plain_text), str(ic)))

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
                chiSquare = ChiSquare(plain_text)
                chi = chiSquare.output()
                ic = chiSquare.ic
                print('%s | %s | %s' % (str(key), str(ic), str(chi)))

                if ic > 0.065:
                    print(ic)
                    print(plain_text)
                    with open('vigenere.txt', 'a') as results_file:
                        results_file.write('%s | %s | %s | %s' % (str(key), str(plain_text), str(ic), str(chi)))
            except:
                time.sleep(0.1)
                print('[!] run finished')
                break
        print('ending worker')
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
    cipher_text = open('cipher_3_text.txt', 'r').read()
    cipher_text = ''.join([x for x in test_cipher_text if x.isalpha()])
    for each in range(9,900,9):
        run = Run(each, cipher_text)
        run.start_single_core()
