import collections
# mono-alphabetic substitution cipher = each letter represents a difrent letter
# a transposition cipher. = plain text is reordered
# enigma machine

# Random IC = 0.0385
# Italian IC = 0.738

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

cipher_text = 'WJHZR DIAKZ TMCYS OMLVY HISNF BNZRP' \
              'OESFJ RVLWL MIPOA LJAKD SQWLH KYSCN' \
              'RMHPB OQNQQ MNBXC CACJN BOVVT LAUWJ' \
              'RNISI FFBJO WZWIV NCWQM AUEEX TNOMR' \
              'JIIYH ISNWD Y'
next_cipher_text = 'WASIRRPDYPMCTNJNERSZDVLUUSGCSPFWQMQHUVZDVLUUSGCSPFWQMQHUVRUNDMMKXTKHWOIEIYMNYCUKTTRFBROEVPLPGTUQTMCLLJWSJGVNHDHXLM'

wax_on =  'LRFKQ YUQFJ KXYQV NRTYS FRZRM ZLYGF' \
          'VEULQ FPDBH LQDQR RCRWD NXEUO QQEKL' \
          'AITGD PHCSP IJTHB SFYFV LADZP BFUDK' \
          'KLRWQ AOZMI XRPIF EFFEC LHBVF UKBYE' \
          'QFQOJ WTWOS ILEEZ TXWJL KNGBQ QMBXQ' \
          'CQPTK HHQRQ DWFCA YSSYO QCJOM WUFBD' \
          'FXUDZ HIFTA KXZVH SYBLO ETSWC RFHPX'


wax_off = 'NUFTD WHFTW HFQUU VZXCX FFTNA XMHMT' \
          'MHFHC XFFTZ AHXMT YUCXM HHAXN TFXNJ' \
          'HZTNX VATCU ZUNAH ATNTZ XDFTZ MUTUA' \
          'ZAXMH LXCNT NXACX WXMUN FVTNH OCTDH' \
          'YUCFQ UTRZH CXFFT ZATCX FFQHV MUHZD' \
          'UVZXD ATCHX YHFFT NXTRC XZMUF QUDHX' \
          'ZXCCX ZAUHJ XCHXD YUAAH MUNFT DWTVD' \
          'XZMTV ZNHZR VXRRH TXJTN AUDFH UZAHL' \
          'HFTWX XZFQU UDTYC XAAVA ATXFX CXAAU' \
          'CUFTW HFTTR ZHCXF FTZAT QXVZH ZACTM' \
          'VGHTZ ULTZM XWUZA XNUXW HTXJJ HDTFQ' \
          'UDYHU RXXRC XZMHN HZUUM TJUDX CXWOH' \
          'UZAXA XNXZX CCXGH TZUDY UDTTU JTNUZ' \
          'AHUCH DTZTM XAHDF HUZAH LHFHF QUMXZ' \
          'ZTVZH MUXMU NNXCR TWUZA TFVHR HCUCX'

class CheckIC:
    def __init__(self, text):

        self.text = text.replace(' ', '')
        self.text = ''.join(e for e in self.text if e.isalnum())
        self.text = ''.join([i for i in self.text if not i.isdigit()])
        self.text = self.text.upper()
        self.text_size = len(self.text)
        self.text_count = collections.Counter(self.text)
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.E = 0
        self.T = 0
        self.A = 0

        self.unseen_alphabet = self.alphabet

        self.ic = self.run()
    def run(self):
        freqsum = 0
        for key, value in self.text_count.items():
            self.unseen_alphabet = self.unseen_alphabet.replace(key, '')
            if key is 'E':
                self.E = value/self.text_size
            if key is 'A':
                self.A = value/self.text_size
            if key is 'T':
                self.T = value/self.text_size

        for letter in self.alphabet:

            freqsum += self.text_count[letter] * (self.text_count[letter] -1)

        self.ic = freqsum / (self.text_size*(self.text_size-1))
        return float(self.ic)


    def print_ic(self):
        print('[IC] %f' % self.ic)


# checkIC = CheckIC(english)
# x = checkIC.run()
# print(x)
# WaxOn = CheckIC(wax_on)
# print(WaxOn.run())
# WaxOff = CheckIC(wax_off)
# print(WaxOff.run())
#WaxOn.print_ic()

