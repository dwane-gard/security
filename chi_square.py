from co_incidence_index import CheckIC

class CheckText:
    def __init__(self, plain_text):
        alphabet = [x for x in'ABCDEFGHIJKLMNOPQRSTUVWXYZ']

        self.plain_text = plain_text
        check_ic = CheckIC(plain_text)
        check_ic.run()

        self.chi = [self.CheckLetter(getattr(check_ic, x), len(plain_text), x) for x in alphabet]
        # print([x.result for x in self.chi])
        self.chi_result = sum([x.result for x in self.chi])


    def output(self):
        return self.chi_result

    def print(self):
        print(self.chi_result)

    class CheckLetter:
        def __init__(self, letter_count, text_count, letter):
            self.letter_count = letter_count
            self.text_count = text_count
            self.letter = letter.upper()
            # print(self.letter)
            self.expected_frequency = 0
            self.find_expected_frequency()

            self.result = self.run()

        def run(self):

            expected_count = self.text_count*self.expected_frequency
            result = ((self.letter_count - expected_count)**2) / expected_count

            return result

        def find_expected_frequency(self):
            if self.letter == 'E':
                self.expected_frequency = 0.127

            elif self.letter == 'A':
                self.expected_frequency = 0.082
            elif self.letter == 'B':
                self.expected_frequency = 0.015
            elif self.letter == 'C':
                self.expected_frequency = 0.028
            elif self.letter == 'D':
                self.expected_frequency = 0.043
            elif self.letter == 'F':
                self.expected_frequency = 0.022
            elif self.letter == 'G':
                self.expected_frequency = 0.02
            elif self.letter == 'H':
                self.expected_frequency = 0.061
            elif self.letter == 'I':
                self.expected_frequency = 0.07
            elif self.letter == 'J':
                self.expected_frequency = 0.002
            elif self.letter == 'K':
                self.expected_frequency = 0.008
            elif self.letter == 'L':
                self.expected_frequency = 0.04
            elif self.letter == 'M':
                self.expected_frequency = 0.024
            elif self.letter == 'N':
                self.expected_frequency = 0.067
            elif self.letter == 'O':
                self.expected_frequency = 0.075
            elif self.letter == 'P':
                self.expected_frequency = 0.019
            elif self.letter == 'Q':
                self.expected_frequency = 0.001
            elif self.letter == 'R':
                self.expected_frequency = 0.06
            elif self.letter == 'S':
                self.expected_frequency = 0.063
            elif self.letter == 'T':
                self.expected_frequency = 0.091
            elif self.letter == 'U':
                self.expected_frequency = 0.028
            elif self.letter == 'V':
                self.expected_frequency = 0.01
            elif self.letter == 'W':
                self.expected_frequency = 0.024
            elif self.letter == 'X':
                self.expected_frequency = 0.002
            elif self.letter == 'Y':
                self.expected_frequency = 0.02
            elif self.letter == 'Z':
                self.expected_frequency = 0.001


if __name__ == '__main__':
    plain_text = '''So my story starts on what was a normal day taking calls on the front line for a large cable company. The job pays well and for the most part the people I deal with are fairly nice to talk to.
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
Anyway thanks for reading just thought I'd share how this one call changed my outlook on life :)'''
    plain_text = ''.join([x.upper() for x in plain_text if x.isalpha()])
    checkText = CheckText(plain_text)
