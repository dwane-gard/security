

with open('10results.txt', 'r') as results:
    results = results.readlines()

best_ic = 0.05

for each in results:
    ic = each.split('|')[-1]

    if ic < best_ic:
        best_ic = ic

print(best_ic)
