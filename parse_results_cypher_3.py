

with open('10results.txt', 'r') as results:
    results = results.readlines()

best_ic = 0.05

for each in results:
    try:
        ic = each.split('|')[2]
        # print(ic)
        # print('*'*10)

        if float(ic) > best_ic:
            print(ic)
            best_ic = ic
    except:
        pass


print(best_ic)
