# from co_incidence_index import derp
from corpus_analysis import Analyse

class encode:
    def __init__(self, cipher_text, key):
        # self.cipher_text = cipher_text
        self.plain_text = ([cipher_text[i:i+2] for i in range(0, len(cipher_text), 2)])
        self.cipher_text = ''
    def run(self):
        # Step 1
        print(self.plain_text)
        self.cipher_text = self.plain_text

        # Add a padding 'X' if required
        self.cipher_text = [x[0] + 'X' if len(x) == 1 else x for x in self.cipher_text]
        print(self.cipher_text)

        # Split up doubles with an 'X' if required
        self.cipher_text = [x[0] + 'X' + x[1] if x[0] == x[1] else x for x in self.cipher_text]
        self.cipher_text = ''.join(self.cipher_text)
        self.cipher_text = ([self.cipher_text[i:i+2] for i in range(0, len(self.cipher_text), 2)])
        print(self.cipher_text)

        # Remove unneeded padding
        if self.cipher_text[-1] == 'X':
            del self.cipher_text[-1]

        print(self.cipher_text)

        # Step 2







        # for each_digraph in self.plain_text:
        #     if len(each_digraph) == 1:
        #         each_digraph += 'X'
        #
        #     if each_digraph[0] == each_digraph[1]:
        #         each_digraph = each_digraph[:1]
        #         each_digraph += 'X'
        #         print('here')

        # self.cipher_text = self.plain_text



        return

    def check(self):
        return

    def output(self):
        print(self.cipher_text)
        return

if __name__ == '__main__':
    plain_text = 'hidethegoldinthetreestump'
    key = 'a'
    plain_text = plain_text.upper()
    run = encode(plain_text, key)
    run.run()
    run.check()
    run.output()
