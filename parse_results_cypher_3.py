

with open('9results.txt', 'r') as results:
    results = results.readlines()
    # print(results)
best_ic = 0.05
top = None
for each in results:
        try:
            if float(each.split('|')[2]):
                ic = float(each.split('|')[2])

                print(ic)

                if ic > best_ic:
                    print(ic)
                    best_ic = ic
                    top = each
        except IndexError:
            pass
            # print('[!] IndexError')
        except ValueError:
            print('[!] Not a float')


print(best_ic)
print(top)
