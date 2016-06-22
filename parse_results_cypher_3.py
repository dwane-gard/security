

with open('10results.txt', 'r') as results:
    results = results.readlines()
    # print(results)
best_ic = 0.05

for each in results:

        ic = float(each.split('|')[2])
        print(ic)
        print('error reading')


        if ic > best_ic:
            print(ic)
            best_ic = ic





print(best_ic)
