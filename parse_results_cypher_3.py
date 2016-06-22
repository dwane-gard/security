

with open('10results.txt', 'r') as results:
    results = results.readlines()

best_ic = 0.05

for each in results:
    try:
        ic = each.split('|')[-1]

        if float(ic) < best_ic:
            best_ic = ic

    except:
        pass
print(best_ic)
