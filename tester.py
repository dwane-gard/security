with open('cipher_3_text.txt') as cipher:
    cipher = cipher.read()

cipher = ''.join([x for x in cipher if x.isalpha()])

for each in range(2,len(cipher)+1,1):
    if (len(cipher)/each).is_integer():
        print(each)
