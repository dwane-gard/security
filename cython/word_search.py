class WordSearch:
    def __init__(self):
        self.keys = open('sowpods.txt', 'r').readlines()
        self.keys = [x[0:-1].upper() for x in self.keys]
        self.keys = [x for x in self.keys if x != 2]
        self.keys = [x for x in self.keys if x != 3]

    def run(self, plain_text):
        word_list = []
        for each_key in self.keys:
            if each_key in plain_text:
                word_list.append(each_key)
            pass
        words_list_len = len(''.join(word_list))
        words_len = words_list_len/len(plain_text)

        return words_len






