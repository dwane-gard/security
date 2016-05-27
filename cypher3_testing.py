
cipher_text = open('cipher_3_text.txt', 'r')

cipher_text = cipher_text.read()
cipher_text = (cipher_text.replace(' ', ''))
cipher_text = cipher_text.replace('\n', '')

cipher_text = cipher_text.split('X')
for each in cipher_text:
    print(each)

