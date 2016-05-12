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
        self.result_coeffienet = 0
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
            if each.frequency > 0 and each.known_frequency > 0:

                each.frequency_per = each.frequency/len(self.ze_text)

                if each.known_frequency*0.9 < each.frequency_per and each.known_frequency*2 > each.frequency_per:
                    self.result += 1

        self.result_coeffienet = self.result/len(self.ze_text)


    def output(self):
        print(len(self.ze_text))
        print(self.result)
        print(self.result/len(self.ze_text))

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
            self.frequency_per = 0
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
    text2 = '''
    So my story starts on what was a normal day taking calls on the front line for a large cable company. The job pays well and for the most part the people I deal with are fairly nice to talk to.
Quite often we'll get calls from seniors (especially in the morning) who have premise equipment issues such as "snow on screen" or "no signal" on their TV sets connected to our digital equipment.
Now my heart does go out to some of these folk because up until recently (past few years) we would supply straight analog cable to many homes (coax direct from wall to TV with scrolling guide). However most cities we service nowadays require our digital equipment to receive channels, and this has caused a lot of frustration with older people who don't know how to operate said equipment (ie. always having your TV set on "video" or "hdmi" to get picture). So often times we get customers who are repeat offenders with long ticket histories of these types of issues.
So anyway, I get a call from an older gentleman who's quite bitter and mean right off the bat (doesn't like that I asked for his address / telephone number to verify the account, hates that he has to speak with a machine before reaching an agent, etc.). I have some experience handling these types of customers, however this call was going to be a little different.
I spent over 45 minutes with this guy (we'll call him Mr. Smith) trying to get his TV set connected to the digital box properly so he could receive a picture. No luck. He was getting clearly frustrated by the whole ordeal and started blaming me for not being able to do my job properly, how I was useless, etc.
Whatever.
Like I said, I've dealt with this before so I tried my best not to take it personally, but eventually I had to ask him if we could book a service tech to the home (a courtesy call) to get his TV working correctly. Unfortunately, our booking calendar was showing an appointment 3 days out. That's when he dropped this on me:
"Don't bother sending a goddamn technician, because I'll be dead by then. I'm 94 and TV is the only thing I have left, are you really going to make me wait for a tech?"
I instantly felt bad. I mean, I've heard every complaint in the book as to why people don't want to wait for a tech but this one kind of got to me. I'm in my mid-20's so honestly I can't even imagine how it must feel to utter those words.
So I spoke with my supervisor, who said they'd see if we could get someone out earlier...but we couldn't promise anything. So I let Mr. Smith know and he was predictably not very happy with my answer.
At that point it almost sounded like he started to cry and went into how he has no family left, and no friends that come visit (this was after I asked if there was anyone in his building that might be able to help). Man. I felt terrible, so I took it upon myself to ask Mr. Smith if I could pay a visit (he lived in a small city over from where I was, not very far to drive).
He was a little shocked I was willing to do this, but sounded thankful I was willing to come out and help him personally.
So I head over, get to the residence and meet him - within 30 seconds I had the cable running again (simple input change) and even brought him a simplified remote for his set top box to avoid this problem in the future.
That's when he started crying. He goes into how he hasn't actually spoken or really interacted with anyone for years. He gave me a hug and told me how thankful he was that I came out and helped him, and told me how sorry he was for being so mean earlier on. I said it was no problem and I was happy to help, and that was it - I left.
3 weeks later, my supervisor comes to my desk and asks me if I could come speak with her for a bit about an account for "Mr. Smith". Turns out, he sent the cable company a letter outlining how thankful he was for helping him with his issue and how it really "made an old man happy again for once in a very long time". The letter was framed and put on our front entrance to retail.
I guess the moral of this story is no matter how nasty someone is to you over the phone, sometimes they're not always a terrible person and just going through a lot. I still think about Mr. Smith occasionally when I get those nasty customers and it makes me feel a little better.
Anyway thanks for reading just thought I'd share how this one call changed my outlook on life :)
'''

    text3 = '''
After reading this tale by /u/jayykidd , it brought back memories of a client of my own that was Paranoid and Rightly So (as an aside, /u/jayykidd , we are totally making PARS a thing around here).
As a bit of backstory, I spent five years doing IT consulting in a rural town about an hour from Portland, OR. I worked for a small company with a few other consultants and a couple of bench techs. My job was primarily server/network engineering-centric, but having done my time as a front-line tech I'd periodically involve myself in the more interesting/complex cases we'd see from our walk-in customers.
One day we had a woman come in. She caught my eye because she was in her late thirties or early forties, and actually quite attractive. She had short, platinum blonde hair and bright red lips, and was dressed and styled like she was transplanted right out of a 1950's era magazine ad. One of our bench techs greets her and starts talking to her. Right out the gate I can tell she is panicked and, by the sound of it, tin-foil hat levels of crazy. Shit, there goes any desire I had to flirt with her and maybe see if I could buy her a drink. I listen in on the conversation anyways, because it's at least a change of pace from the monotony of my day-to-day.
After a few minutes of her going on about how her husband is spying on her through all manner of devices, my bench tech looks back at me with a can-you-please-come-help-me-and-make-her-go-away look on his face. I oblige, as I appreciated that the front-line guys respected me enough to ask for my help on these things. I walked up front, introduced myself as the supervisor, and told her that since her issue was so unique and serious it'd probably be best if our more senior staff handled it. Now that I was seeing her up close, I could tell that under her classy outfit and Marilyn Monroe-esque makeup was a deeply distraught woman. Her eyes looked baggy, and tired. Like she had been up too late crying.
Obviously, at this point I'm just playing along. This isn't my first rodeo, and generally what happens is the client claims some individual or three letter agency is monitoring their computer, we tell them our hourly rate for forensics ($150 an hour), and suddenly the men-in-black-suits watching them aren't that big of a deal anymore. Now, to be fair, we actually did specialize in computer forensics and data recovery, working extensively with the local police department and a handful of legal firms on a number of cases where they needed expert help, we even had a guy on staff full-time who wore that hat most days. The local police were pretty small-time and farmed out at least some of their computer crime related work to us on contract. In the cases where people did want to pay, we would do our due diligence, and prepare a professional report of our findings accordingly. We would meet with attorneys and testify in court, as necessary. Generally it was fairly benign stuff like gathering chat logs and browser history for a divorce proceeding where one spouse accused the other of cheating or something similar, and wanted evidence to back that up.
Back to the client at hand. She insists her husband is monitoring her every move, tracking her vehicle, monitoring her computer, and recording her in her own home. Here's where it gets interesting: She claims that she knows all of this, because he has told her about it. In fact, he has gone so far as to threaten her life if she tries to tamper with any of it. She says she has tried to apply for a protective order against him, but ostensibly without some sort of evidence of his behavior, nobody would take her seriously.
I give her the crazy litmus test and I tell her that in order to gather evidence discreetly we would need two of our senior consultants to investigate. $300 an hour, four hour minimum.
She pulls out her wallet.
Fuck, she's serious.
We agree to start with her vehicle to check for signs of the GPS tracker. She says she is parked several blocks away so her husband won't know she came to a computer store (we were in a downtown area surrounded by retail stores). So I grab my toolbag and holler at one of my colleagues (who has been tuned in himself from his back office desk) to join me.
So the lady, myself, my colleague, and BOTH of our now intensely curious bench techs (all of us in matching company polos) follow this lady down the street to her car. What a motley crew we must have been. We get to her minivan begin our process of looking for this GPS device. Now, GPS trackers (at least the commercially available ones) require two things, generally: dedicated 12v power and an unobstructed (at least by metal) view of the sky. They basically use GPS to grab the coordinates and then a GSM/CDMA (cellular) signal to relay the positional data to a web interface or something. So there really aren't that many places they can really be mounted that are both effective and discreet. We spend some time looking around the undercarriage, rocker panels, and even bits of the interior. Battery doesn't have any additional leads running off of it, fuse box isn't tapped anywhere for power. Nothing. Just as I'm starting to lose faith that this may not be quite as exciting as I had perhaps hoped, I find the fucking thing.
It was tiny, not much bigger than a flash drive, and mounted behind the front grille. It looked pretty much exactly like this.
The reason it didn't need auxiliary power is that it wasn't an active device. This device did not provide real-time tracking, rather it used some internal memory and a couple AAA batteries to log GPS data for days at a time. At some point, when the van was not in use, the guy would grab the GPS device, upload the data to his laptop, maybe swap batteries, then remount it to the car.
Fucking hell, this lady was very much indeed Paranoid And Rightfully So.
Now that we've established that she isn't batshit insane but that she actually is being tracked by her husband, the tone amongst our team became drastically more serious. Obviously, something sinister is going on, and we aren't sure what, but by the sound of things this lady really is fearful of her life. She has entrusted us to gather evidence and help her get a protective order against him, which is something I think all of us took quite seriously.
We show her the tracker and she breaks down into tears because it's the first evidence she has physically seen. We take photos of it, and carefully install it back where it belongs. I sort of assumed that a GPS tracker on your fucking car would be proof enough for a judge to issue at least a temporary protective order, but she seemed insistent that she would need more evidence to make it stick.
Our next moves have to be conducted very deliberately. She claims that her home is bugged, and so is her computer. We will need to go onsite to investigate accordingly, but it will have to be at a time when both her husband isn't home and when we will be able to quickly create a report for her, leaving her enough time to get a protective order before the day's end. We couldn't chance him coming home later, reviewing whatever it was he was recording, and finding out that she had taken action to have him investigated.
It wasn't going to be for at least a week before there was a time that was just right. We made arrangements with her back at the office and I offered to walk her back to her car. She accepted, and on the way she confided in me many of the personal details of her life and her obviously abusive relationship with her husband. In the interest of protecting her privacy I'll simply say that it sounded like she finally figured out how manipulative he was, and when she said she wanted out he wasn't about to let that happen. I asked her again if she really was afraid for her life, and the sincerity of her "yes" was both scary and heartbreaking for me. I asked her if she had thought about getting a gun, and she said she had, but that he would notice the large sum of money needed to purchase one missing from their joint account.
As the gravity of the situation weighed on me, I offered to let her borrow one of mine. She was awestruck, but I assured her that it was completely okay. At the time, I had several handguns and rifles, and I couldn't think of a more appropriate situation for someone to have one. My car was parked close by, and we walked over to it. I tried to gather some idea of her familiarity with guns, as the thought of giving one to more or less a complete stranger, especially one that might not know what to do with it, was unsettling to me. It sounded like she had at least a basic understanding of their function, had gone shooting before, etc. In my mind the pros of her having at least some means to protect herself outweighed the cons, so I moved forward. In the trunk, I had a Ruger LCP, which is a very small .380 caliber handgun that I kept in my Get Home Bag/emergency survival kit. It was fitted with the factory installed Crimson Trace laser grips, which I had dialed in to about 10 meters. We went over the basics of how to use it safely, I showed her how the laser worked, and told her that, for her situation, all she had to know was that the bullet would go more or less where the red dot of the laser was. She was crying, and frankly at this point I pretty much was, too. I gave her my cell phone number and told her to call me if she needed someone to talk to. We hugged for a while before parting ways. It wasn't a romantic hug or anything, it was that kind of hug that's exchanged when someone needs to be held. Like, when your best mate tells you his mom passed away or something. She needed the comfort of knowing that she wasn't alone, that at least one person took her seriously, and I'd like to think that I gave her some hope that things would be okay.
The next week was tense, as we prepared for our investigation. My coworkers and I spent considerable time discussing and researching ways to triage her computer to look for evidence, as well as how to approach the search of the house. When the day finally came, we arrived onsite at the specified time armed with our forensics tools, flashlights, laptops...anything we might need.
I set to work immediately on her computers (a home desktop and a personal laptop) while two of my colleagues began their search of the house. I removed the drives from her PCs, and using a USB write-blocker, (which physically prevented me from writing/modifying any information on her drives) I made a clone of both drives. For the sake of speed, both drives were cloned to SSDs. Once cloned, I put the PCs back they way they were and began mounting the cloned volumes and investigating. The drives were mounted into a quarantine VM, with no WLAN access. Scanning the drives with a number of antimalware programs didn't turn anything up. Looking through the file system however (paying special attention to hidden files and protected system files), turned up some things that didn't look quite right (filenames and directories that looked obfuscated). I made the call to boot up both PCs off of the cloned SSDs and look that them live to see if maybe I could catch an obfuscated process running, or something.
Nothing.
With nothing else open, I ran a netstat -an out of CMD. There were a handful of TCP connections active. One by one, I started performing DNS lookups on the IPs. Everything was normal active connections for background processes like Skype. Then, I found it. An active connection to a clearly obfuscated domain name. It looked like a license key with a .com at the end of it. Something like 24W25-188EGFF-98001QRD.com.
It was hiding in plain sight, and it was registered to SpectorSoft Corporation. Guess what they sell? Yup. Surveillance software.
The PC was running something called Spector Pro, which was capable of monitoring all of the users activities, browsing history, keylogging, even sending remote screen captures to a mobile phone or email based on target keywords. It was the full nine yards for monitoring.
I screen capped everything for my logs, shut the system down, and swapped the forensic SSDs for the original disks to put everything back the way it was.
Not too long after, our other two guys found some evidence of their own. Two separate (and frankly, rather rudimentary) CMOS cameras hidden in the master bedroom. One in the closet in a shoebox, one in the smoke detector in the ceiling. Both, if I recall correctly, were simply wired to 9V batteries and recorded to SD cards. All things considered, they were pretty low tech. The contents of the memory cards would have had to be moved off at least once a day, and the battery probably changed at least as often.
We didn't touch anything. Lots of photographs were taken. We went back to the office and compiled all of the evidence into a document for her, and I passed the disk images onto our forensics guy for further evaluation. I met with the client later that day to present her the report so she could furnish it to the court.
The gratitude she had for us was absolutely immeasurable. We didn't charge her for our services. Getting to play a role in stopping her sick fuck of a husband from engaging in whatever it is he was doing was payment enough.
I'd like to tell you that I know how this story ends. I'd like to say that the guy was put away in jail forever, and my supreme IT prowess and white-knightery wooed her into my arms and we lived happily ever after. But frankly, I don't really know what happened. What I can tell you that about a week after we gave her our report, I met her for coffee at a place across the street. She looked visibly better. Her puffy, tired eyes were gone, replaced instead by ones that seemed to glisten with warmth. Her skin was radiant and beautiful. She was smiling, for the first time I'd seen. An immense weight had been lifted off of her, and it showed. She told me that she was temporarily living with her mom and dad, that a restraining order was in place on her estranged husband, and that she was finally filing for divorce. She told me that for the first time in a very long time she felt safe, and that she felt happy.
In the parking lot, she gave me back the little handgun, profusely thanking me again for the work we did. She hugged me, both of us teary-eyed, and we parted ways. For me, it proved to be one of the most emotionally rewarding experiences of my career.
Edit: Thank you to everyone who's gilded this post! It's definitely put a smile on my face.
'''
    text_jumble = '''
    COOUS ULYDU TQOHY SEELP EUTST GTOAR
        IDTHM WPEER DTTEF EXUTO ROSEC UYCOU
        DUBEU LUONL IKFTE YHCER LROTU ESAOF
        ANRAI EQSOR ETLER HTFTE UISEI SDQBY
        LSFOS ERTIN NRGED AWTOR KLEQA IASNT
        RFEXL OASMP TBOTW UHEER ISTWD EOIUL
        ETASV LTAGI UYAST OTEAR PNOIN GNITI
        HOEDY TETCR OTNQT IUPES ROKEY MNTLA
        ITNKS HIITI OHNLC EYTDE ANNDH TREIG
        ITNGO HTTOD OONAH DTTET LMLIO IOENS
        LDLAO ORFSY DMEFS ARUOM ILNGO LEENR
        OSCKO TBNEF HEECA TORMP EYCLD DANRE
        KARUY NPBTC UONDC FSTSU EANRM SOHNE
        YLEEN OTPRA IIOND TFSUN RNEAH DCAHT
        ETNET BFAIT OEMPS CAHNY LMOYW PEEES
        OOSTI LTHHE TRIRN EERME VSINN AGTSA
        OPVIE RDDER FITOI ELLOW MCECU OONNS
        SEINI RCMAL NOIAC RWFHO ANFFT TOARD
        YPTHE AEOIR GEYBS RINLL VIESI NTIED
        UYRCA OONMP EYCAI BUNSE IEEVN LEBDI
        ONNAT RNEDI NFANL ICSIA TTEMS AESNT
        NAOTK MSIEE TNORV GEICO YRLON MSETI
        TEMEU SNVTB OIBEV DLTIE ATTYE HOEUR
        OPYEE LEMSD VEEMA RUSCH RTTHY EEFIR
        SAOFD RHEAR KOMAG RKWIN ONNAO RNEDY
        CRHIW IKUNO WOILV ULYNE ERADS RTEHI
        IMLAO ANEDC NLTBT DEUBO EEDWI RIHTH
        TBUNS ULTES AOREL UWYIL TNOHY GAIVE
        NUAMD REOGO IWNAI NMOER HAISY NTCOR
        NSEOS OFAIT SOEBN RUWSI CSRIA SMEIN
        OSUHA YALVE NHCET ANCOW GRHTG IAONE
        IEOUO GSRWR NGDEH IENDW YLOUT ENIET
        EDLLR WOEVE LMLIA IOANM FYENS ORNON
        LMOYW PEEES FRINI EAENC YLDET LVAAS
        DTWHH EEANT MCPAE ONEYD RLEDK ABCAN
        TUCYT PARND REREE ITHIR TEPLW NAMNS
        WRIPU EEEDO DAENM NRTON ADNAO ESATR
        IOCAO MLNPR DIURT TIFNG AELIN CFHOR
        NAERR EGIYC SSLAE ISITY SRARL AEASU
        ETRET HATRE SOANF UDHSO SOUMW NECRS
        ROEUL ANHAB PTAYI OTEHE SBICR AERNE
        IYLLD BSGAN LHART EGTES LTITT IYUIN
        TEATB SEHIS RNUPE KTATH YEORM WKNTI
        ESPOD RRETE THYOL AUTSO LMLIO IODNW
        OTFEN HNRRO CTKWE OHSIL RGESE GSAIV
        RYGIH UNLGT MCPAE ONEYS OPYEO LEMST
        PEBUG EYKIN OTNAH DTIET OSNET MYITO
        UENDT FSHSE OPHEE TLUPR RATHV IEPLI
        FSTHA OOESE IECAU RNMSH YTENS BRRON
        ENRHE DAUND DANEI NFDAR DUEAG SLOIN
        HOERE TWSIS WOILV ULYHA SLTAE OLELR
        CPTFM ERSOM DNECH YEANT WRORG DKAIN
        TNRUN DSATI EARIS MCGAN HFOMT WYOOU
        AODVA KAONT AEYGA MOGDH EERCY MYVON
        SUOUN RLOSI EELYI RCCHR ATNWN ICSHU
        '''

    analyse = Analyse(text)
    analyse.run()
    analyse.output()
    analyse2 = Analyse(text2)
    analyse2.run()
    analyse2.output()
    analyse3 = Analyse(text3)
    analyse3.run()
    analyse3.output()
    jumble = Analyse(text_jumble)
    jumble.run()
    jumble.output()






