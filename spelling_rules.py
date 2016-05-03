from string_check import BoyerMoore

class SpellingRules:
    def __init__(self, text):
        self.text = text
        self.break_count = 0
        self.major_break_count = 0

    def I(self):

        I_results = BoyerMoore('I', self.text).search_results


        if self.text[I_results + 1] is not 'E':
            if self.text[I_results - 1] is not 'C'

    def Q(self):

        Q_results = BoyerMoore('Q', self.text).search_results

        if self.text[Q_results+1] is not 'U':
            self.break_count += 1
            self.major_break_count += 1


