import collections



class Kasiski:
    def __init__(self, cypher_text):
        cypher_text = cypher_text.replace(' ', '')
        self.original_cypher_text = cypher_text
        self.multiples_list = []

        cypher_text = self.original_cypher_text
        longest_string = ''
        x = 0
        while x < 8:
            key_size = 3
            while key_size < 8:
                cypher_list = [cypher_text[i:i+key_size] for i in range(0, len(cypher_text), key_size)]
                # print(cypher_list)

                for each_string in cypher_list:
                    if cypher_text.count(each_string) > 1:
                        ze_split = (len(self.original_cypher_text.split(each_string)[1]))
                        print(each_string)
                        print(ze_split)
                        local_multiples = []
                        for each in self.multiples(ze_split+len(each_string)):
                            if each in self.multiples_list:
                                local_multiples.append(each)
                        self.multiples_list = local_multiples


                key_size += 1

            cypher_text = cypher_text[1:]
            x += 1

        # print(longest_string)



        print("[key length is either]")
        print(self.multiples_list)


    def output(self):
        return self.multiples_list

    def multiples(self,n):
        multiples_list = []
        for each in range(n+1):
            for each2 in range(n+1):
                if each * each2 == n:
                    print(each, each2)
                    if each not in multiples_list:
                        multiples_list.append(each)
                    if each2 not in multiples_list:
                        multiples_list.append(each2)
        for each in multiples_list:
            if each not in self.multiples_list:
                self.multiples_list.append(each)
        return multiples_list



if __name__ == '__main__':


    cypher_text = '''CVJTNAFENMCDMKBXFSTKLHGSOJWHOFUISFYFBEXEINFIMAYSSDYYIJNPWTOKFRHWVWTZFXH
LUYUMSGVDURBWBIVXFAFMYFYXPIGBHWIFHHOJBEXAUNFIYLJWDKNHGAOVBHHGVINAULZFOF
UQCVFBYNFTYGMMSVGXCFZFOKQATUIFUFERQTEWZFOKMWOJYLNZBKSHOEBPNAYTFKNXLBVU
AXCXUYYKYTFRHRCFUYCLUKTVGUFQBESWYSSWLBYFEFZVUWTRLLNGIZGBMSZKBTNTSLNNMD
PMYMIUBVMTLOBJHHFWTJNAUFIZMBZLIVHMBSUWLBYFEUYFUFENBRVJVKOLLGTVUZUAOJNVU
WTRLMBATZMFSSOJQXLFPKNAULJCIOYVDRYLUJMVMLVMUKBTNAMFPXXJPDYFIJFYUWSGVIUM
BWSTUXMSSNYKYDJMCGASOUXBYSMCMEUNFJNAUFUYUMWSFJUKQWSVXXUVUFFBPWBCFYL
WFDYGUKDRYLUJMFPXXEFZQXYHGFLACEBJBXQSTWIKNMORNXCJFAIBWWBKCMUKIVQTMNBC
CTHLJYIGIMSYCFVMURMAYOBJUFVAUZINMATCYPBANKBXLWJJNXUJTWIKBATCIOYBPPZHLZJJZ
HLLVEYAIFPLLYIJIZMOUDPLLTHVEVUMBXPIBBMSNSCMCGONBHCKIVLXMGCRMXNZBKQHODESY
TVGOUGTHAGRHRMHFREYIJIZGAUNFZIYZWOUYWQZPZMAYJFJIKOVFKBTNOPLFWHGUSYTLGN
RHBZSOPMIYSLWIKBANYUOYAPWZXHVFUQAIATYYKYKPMCEYLIRNPCDMEIMFGWVBBMUPLHML
QJWUGSKQVUDZGSYCFBSWVCHZXFEXXXAQROLYXPIUKYHMPNAYFOFHXBSWVCHZXFEXXXAIR
PXXGOVHHGGSVNHWSFJUKNZBESHOKIRFEXGUFVKOLVJNAYIVVMMCGOFZACKEVUMBATVHKID
MVXBHLIVWTJAUFFACKHCIKSFPKYQNWOLUMYVXYYKYAOYYPUKXFLMBQOFLACKPWZXHUFJYG
ZGSTYWZGSNBBWZIVMNZXFIYWXWBKBAYJFTIFYKIZMUIVZDINLFFUVRGSSBUGNGOPQAILIFOZ
BZFYUWHGIRHWCFIZMWYSUYMAUDMIYVYAWVNAYTFEYYCLPWBBMVZZHZUHMRWXCFUYYVIEN
FHPYSMKBTMOIZWAIXZFOLBSMCHHNOJKBMBATZXXJSSKNAULBJCLFWXDSUYKUCIOYJGFLMBW
HFIWIXSFGXCZBMYMBWTRGXXSHXYKZGSDSLYDGNBXHAUJBTFDQCYTMWNPWHOFUISMIFFVXF
SVFRNA'''
    cypher_text = 'WJHZR DIAKZ TMCYS OMLVY HISNF BNZRP' \
                  'OESFJ RVLWL MIPOA LJAKD SQWLH KYSCN' \
                  'RMHPB OQNQQ MNBXC CACJN BOVVT LAUWJ' \
                  'RNISI FFBJO WZWIV NCWQM AUEEX TNOMR' \
                   'JIIYH ISNWD Y'

    # cypher_text = 'JVJAHVMDQIUGCJDASTDPHHMPQHYDPQYCAECPWFDSKFJPJLVJEVPRREVHXDHVFGCJDASTDDVAPCTBP'
    Kasiski(cypher_text)
