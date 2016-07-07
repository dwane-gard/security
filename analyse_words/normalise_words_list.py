words_file = open('sowpods.txt').readlines()
new_words_file = open('new_sowpods.txt', 'a')
for each in words_file:
    each = each.upper()
    each = each[0:-1]
    # print(each)
    new_words_file.write(each)
