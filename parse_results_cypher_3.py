

with open('10results.txt', 'r') as results:
    results = results.readlines()
    # print(results)
best_ic = 0.05

for each in results:
        try:
            ic = float(each.split('|')[2])
            print(ic)



            if ic > best_ic:
                print(ic)
                best_ic = ic
        except IndexError:
            print('IndexError')
            print(each)






print(best_ic)
