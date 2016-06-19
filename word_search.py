
class WordSearch:
    def __init__(self, message):
        self.word_list = []
        self.words_len = 0
        self.message = message
        self.message_length = len(message)
        self.keys = open('sowpods.txt', 'r').readlines()

    def run(self):
        for each_key in self.keys:
            if len(each_key) == 2:
                continue
            if len(each_key) == 3:
                continue
            else:
                if each_key in self.message:
                    self.word_list.append(each_key)

        self.words_len = (len(''.join(self.word_list))/self.message_length)






