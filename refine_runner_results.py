f = open('results.txt').readlines()

for each_line in f:
    each_line = each_line.split('|')
    if float(each_line[2]) > 0.9:
        print(each_line)
        print('\n')

