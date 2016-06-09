# mono-alphabetic substitution cipher = each letter represents a difrent letter
# a transposition cipher. = plain text is reordered
# enigma machine

# Random IC = 0.0385
# Italian IC = 0.738


class CheckIC:
    def __init__(self, text):

        self.text = text.replace(' ', '')
        self.text = ''.join(e for e in self.text if e.isalnum())
        self.text = ''.join([i for i in self.text if not i.isdigit()])
        self.text = self.text.upper()
        self.text_size = len(self.text)

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
        self.letters = []
        self.ic = 0
        self.unseen_alphabet = self.alphabet

    def run(self):
        freqsum = 0

        self.A = self.text.count('A')

        self.B = self.text.count('B')

        self.C = self.text.count('C')

        self.D = self.text.count('D')

        self.E = self.text.count('E')

        self.F = self.text.count('F')

        self.G = self.text.count('G')

        self.H = self.text.count('H')

        self.I = self.text.count('I')

        self.J = self.text.count('J')

        self.K = self.text.count('K')

        self.L = self.text.count('L')

        self.M = self.text.count('M')

        self.N = self.text.count('N')

        self.O = self.text.count('O')

        self.P = self.text.count('P')

        self.Q = self.text.count('Q')

        self.R = self.text.count('R')

        self.S = self.text.count('S')

        self.T = self.text.count('T')

        self.U = self.text.count('U')

        self.V = self.text.count('V')

        self.W = self.text.count('W')
        self.X = self.text.count('X')
        self.Y = self.text.count('Y')
        self.Z = self.text.count('Z')

        self.letters = [self.A, self.B, self.C, self.D, self.E, self.F, self.G, self.H, self.I, self.J, self.K,
                        self.L, self.M, self.N, self.O, self.P, self.Q, self.R, self.S, self.T, self.U, self.V,
                        self.W, self.X, self.Y, self.Z]

        for each_letter in self.letters:
            freqsum += each_letter * (each_letter - 1)

        self.ic = freqsum / (self.text_size * (self.text_size - 1))
        return float(self.ic)


    def run_with_counter(self):
        from collections import Counter
        self.text_count = Counter(self.text)
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

if __name__ == '__main__':
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

    derp = '''ARLHIFIJFIHFBAFONVTIDLEQSOJVEAEJPHQHNHSNALDHHAGEECIMORDSNRQAWEOFSNRDCNSOKRIIMGOTULNPFCTSUSRSDLJOSEMQBVLZRTBJV
DDWUREBSDUVVDZBUPFHPFAGTRMVESXAQWSSRISSMRANVLEFBIVKRSLWTFHKIKMXKLNDPDNAVNFBAQSBBFNWZAFONAFDDWQGOLFAHFRKRHNFARDWZBHTLALL
AGPXOGUVFQLBHNHXIFWTRESBFNOVDCNUFDKDLHBANHASCRDCWHHAISWGISJUMPEYIMVOHBGSQKXVOMBFTGUCIXMYEARGAWSLQLIAAPPLMHREVGRHSSIHFBA
FONVTIDLJSSEMDNVURZXOUVEILMFMOBNVYBIAITMRVHCGRCBUQNOQGCUSUFNOIMAOTGVEAUATSTSPNGILSTIARHPAAVANLUSDACOSELCNGIHSSEMJSWUAPY
USDBFXCSRTGGSAVDLAOPFEFEHSIJFVEAID'''
    import time

    start = time.time()
    checkIC = CheckIC(english)
    checkIC.run()
    checkIC.print_ic()
    end = time.time()
    print(end - start)

    ze_start = time.time()
    checkIC = CheckIC(english)
    checkIC.run_with_counter()
    checkIC.print_ic()
    ze_end = time.time()
    print(ze_end - ze_start)

    ze_start = time.time()
    checkIC = CheckIC(derp)
    checkIC.run_with_counter()
    checkIC.print_ic()
    ze_end = time.time()
    print(ze_end - ze_start)

