import itertools

import time



class Analyse:
    def __init__(self, ze_text):



        self.alphabet = [x for x in 'abcdefghijklmnopqrstuvwxyz']

        ze_text = ze_text.replace('\n', ' ')
        ze_text = ze_text.replace('.', ' ')
        ze_text = ze_text.replace(',', ' ')
        # ze_text = ze_text.replace(' ', '')
        ze_text = ze_text.replace("'", '')
        ze_text = ''.join([x for x in ze_text if x.isalpha()])
        ze_text = ze_text.lower()
        self.ze_text = ''.join([x for x in ze_text if x in self.alphabet or x in ' '])
        self.words = ze_text.split(' ')
        self.result = 0
        # flat list of possible bigrams

                # print('[Name]\t\t %s ' % each.name)
                # print('[Frequncy]\t %s' % str(each.frequency))
                # print('[Known Frequency] %s' % str(each.known_frequency))

                # print(len(f))
    def run(self):
        # Create a list of all possible english bigrams
        all_possible_bigrams = itertools.product(self.alphabet, self.alphabet)
        all_possible_bigrams = list(all_possible_bigrams)
        all_possible_bigrams = [x+y for x, y in all_possible_bigrams]

        bigrams = [] # list of bigram class

        # Create a class for each possible bigram
        for each_bigram in all_possible_bigrams:
            bigrams.append(self.Bigram(each_bigram))

        # Break up the text into words, it is not required for the text to be in words though
        for each_word in self.words:


            print(each_word)
            i = 0

            # If there are still spaces get rid of them
            each_word = each_word.replace(' ', '')

            # Until there are no characters left in the word we are looking at
            while i < len(each_word)-1:

                ze_bigram = each_word[i] + each_word[i+1]
                if len(ze_bigram) == 1:
                    break

                for each_bigram in bigrams:
                    if each_bigram.name == ze_bigram:
                        each_bigram.frequency += 1
                        i += 1
                        break

        bigrams.sort(key=lambda x: x.frequency, reverse=True)
        for each in bigrams:
            if each.frequency > 0:
                each.frequency = each.frequency/len(self.ze_text)
                # print(each.frequency)
                # print(each.known_frequency)
                # print('*'*20)
                if each.known_frequency+0.0035 > each.frequency and each.frequency > each.known_frequency-0.0035:
                    self.result += 1



    class Bigram:
        def __init__(self, bigram):
            self.frequent_bigrams = {
                    'TH': 1.52,
                    'EN': 0.55,
                    'NG': 0.18,
                    'HE': 1.28,
                    'ED': 0.53,
                    'OF': 0.16,
                    'IN': 0.94,
                    'TO': 0.52,
                    'AL': 0.09,
                    'ER': 0.94,
                    'IT': 0.50,
                    'DE': 0.09,
                    'AN': 0.82,
                    'OU': 0.50,
                    'SE': 0.08,
                    'RE': 0.68,
                    'EA': 0.47,
                    'LE': 0.08,
                    'ND': 0.63,
                    'HI': 0.46,
                    'SA': 0.06,
                    'AT': 0.59,
                    'IS': 0.46,
                    'SI': 0.05,
                    'ON': 0.57,
                    'OR': 0.43,
                    'AR': 0.04,
                    'NT': 0.56,
                    'TI': 0.34,
                    'VA': 0.04,
                    'HA': 0.56,
                    'AS': 0.33,
                    'RA': 0.04,
                    'ES': 0.56,
                    'TE': 0.27,
                    'LD': 0.02,
                    'ST': 0.55,
                    'ET': 0.19,
                    'UR': 0.02}
            self.name = bigram
            self.first_letter = bigram[0]
            self.second_letter = bigram[1]
            self.known_frequency = 0
            for key, value in self.frequent_bigrams.items():
                if self.name.upper() == key:

                    self.known_frequency = value/100
            self.frequency = 0


if __name__ == '__main__':
    text = '''
        I was working at a startup telco who was getting into Ethernet tails and IX. We put equipment in a lot of 3rd-party datacentres as they were the best place to connect with ISPs and other carriers.
This particular datacentre was one of the older ones, had been full for years, and the company that operated it had long since focused their attention on their newer, shinier datacentre that it was actually possible to still buy space in. One guy, who I'll call Dick, was responsible for both, and didn't give a crap about the old one. Since there was no structured cabling and it was impossible to get anyone out to install any, people just ran their own cabling under the floor and there were no records as to where any of it went.
I'd visited the room to install a switch, when I noticed that the air-conditioner, which was right next to our rack, had two red lights on its display panel.
MINOR ALARM (x)
MAJOR ALARM (x)
Concerned, I picked up the phone.
chhopsky: Hey Dick, I think there's a problem with the AC down here. It's got a couple of pretty serious looking alarm lights on it and the room is a little warmer than normal. You should probably check it out.
Dick: Oh, okay thanks for letting me know. I'll look into it.
This was his usual response, which was followed up by his usual follow-up which was to do absolutely nothing. Two weeks later I went back to do some patching, and noticed the lights were still on.
chhopsky: Hey, these alarm lights are on again. Just thought you should know, whatever you fixed mustn't have taken.
Dick: Oh okay, thanks for letting me know. I'll look into it.
I sighed, and walked back to the office.
About a month later I was sitting at my desk casually perusing the graphing system, when I noticed that peering traffic was dropping off. Not slowly, but one big chunk at a time, getting lower and lower every few minutes. I raced to find out whether we had a graphing problem, but quickly noticed that for every drop-off in traffic, the router was reporting one less peer. Peers were dropping off the network. But how? IOS bug? Memory leak? Then it hit me.
All of the peers dropping off were in that DC. And they were dropping off in order of proximity to our rack. I called Dick, but his phone didn't even ring, and it didn't go to voicemail, just .. failed. I ran out of the office and sprinted off down the street to the DC. Upon busting through the door, I heard a very weird sound upon taking my first step. It was most definitely a 'splash'.
I looked down, and I was standing in an inch of water. Above a raised floor 30cm deep filled with cables. DIRECTLY NEXT TO THE BATTERY BANK OF THE UPS WHICH WAS OPEN WITH EXPOSED WIRING. Heart jumped into my mouth pounding like a jackhammer. ".... I'm about to die." But I didn't, and I very slowly and carefully took a step back onto dry ground.
Looking up to the end of the row, I saw two tradesmen with some floor tiles up, a pump, and a large dryer.
chhopsky: What the hell happened? Where is Dick and why isn't his phone working?
Tradie: Oh, about three years ago during the yearly service I noticed that the plug cap on the high pressure chilled water loop had developed a crack and was failing. I told Dick about it at the time and he said he'd look into it. I guess he didn't because it was still like this the last two years. We came in to service it this morning and I tapped it to see if it was on tightly .. long story short it literally exploded."
Now, this building was about 40 stories high and we were on level 8. The chillers for the airconditioners were on the roof, so by the time the water is on Level 8, it's REALLY high pressure. When the cap ruptured, water came out so hard and fast that it shot the concrete floor tile (weighing ~20kg at least) up off the floor, and kicked it up to a 45 degree angle, turning the single blast of water into a high pressure sprinkler which liberally doused the first three racks with water.
The first three racks contained the primary and backup core voice switches for the company. FOR THE ENTIRE STATE. Yep, I couldn't call Dick because all mobile services and most fixed-line services for that carrier were down.
The subfloor slowly filled up with water, taking out racks one by one as it hit their power connections. All the copper cabling under the floor was ruined. Hundreds, if not thousands of inter-rack patches, all dead. Thankfully it had stopped 1cm shy of spilling over into the UPS battery bank, which would have killed me instantly.
By sheer luck/preparation, our rack was safe. We were the most 'uphill' on the subfloor, and I had made sure that when our power was installed that I got a 15A Screw-in waterproof connector, and although it was wet, we were very much still operating and still online.
The DC is no longer operating as a 3rd-party room and literally every customer has moved out. Next time I called in, someone else answered Dick's phone, and introduced himself as the new facility manager. I told him I needed to get some fibre patching installed to another floor of the building, and that I'd started the process with Dick but didn't get a response to my last email.
New Dick: Oh okay, thanks for letting me know. I'll look into it.
    '''
    analyse = Analyse(text)
    analyse.run()
    print(len(text))
    print(analyse.result)
    print(len(text)/analyse.result)






