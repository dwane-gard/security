from packages.analyse import Dia, CheckIC, ChiSquare,NthMessage
from packages.pre_analysis import Kasiski
from termcolor import colored

class RailFence:
    def __init__(self, cipher_text, *args):
        # cipher_text = ''.join([x for x in cipher_text if x.isalpha()])
        self.cipher_text = cipher_text
        self.known_text = args

    def analyse(self):
        cipher_text_list = [x for x in self.cipher_text]

        for index, object in enumerate(cipher_text_list):
            if object == 'C':
                print(colored('%s: %s' % (str(index), str(object)),'red'))
            elif object == 'O':
                print(colored('%s: %s' % (str(index), str(object)),'red'))
            elif object == 'M':
                print(colored('%s: %s' % (str(index), str(object)),'red'))
            elif object == 'P':
                print(colored('%s: %s' % (str(index), str(object)),'red'))
            elif object == '3':
                print(colored('%s: %s' % (str(index), str(object)),'red'))
            elif object == '4':
                print(colored('%s: %s' % (str(index), str(object)),'red'))
            elif object == '1':
                print(colored('%s: %s' % (str(index), str(object)),'red'))
            elif object == '{':
                print(colored('%s: %s' % (str(index), str(object)), 'green'))
            elif object == ' ':
                print(colored('%s: %s' % (str(index), str(object)), 'blue'))
            else:
                print('%s: %s' %(str(index), str(object)))


            # #mp
            # first 174
            #
            # for each in [19,120,154,267,278]:
            #
            #     # find the difrence between each
            #
            #     #-101
                #-135

    def pre_analyse(self):
        checkIC = CheckIC()
        cipher_text = ''.join([x for x in self.cipher_text if x.isalpha()])
        print(cipher_text)
        print(self.cipher_text)
        print(checkIC.run(''.join([x for x in self.cipher_text if x.isalpha()])))
        # kasiski = Kasiski
        #
        # for degree in range(1,25):
        #     nthMessage = NthMessage(cipher_text, degree)
        #     print(nthMessage.output())



if __name__ == '__main__':

    railFence = RailFence('''S_   ltes e__owesft4ya'h r_ernadinhohn_hstfeamion coo iost  lhrooidskeutsio t,aPeeut_eemlc tmkhegi_wschoool31neOen Cbale4h s tee_  oi_r yjnsr  iat_.>dslu}4 nd asthsnCg\  it_ Misdirection_tCaeesa Oe1elr__firiOR_lelsmk_hlabsfkabM{fbbliuec_p  eiecn P1oaubco a_ite_headm34rebihchtHo4c'''
                          , 'COMP3441{')
    railFence.pre_analyse()
    # railFence.analyse()