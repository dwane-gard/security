import itertools


client_ip_available = (itertools.product([192], [168], [0], range(1, 255, 1)))
client_ip_available = [tuple([bytes(x)[i:i+1] for i in range(0, len(x), 1)]) for x in client_ip_available]
# client_ip_available = [client_ip_available[i:i+1] for i in range(0, len(client_ip_available), 1)]

for each in client_ip_available:
    print(each)