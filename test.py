

def fence(cipher_text, key_size):
    # Create a list of lists with null values to be filled
    fence = [[None] * len(cipher_text) for n in range(key_size)]

    # Discover the pattern of the zig zag
    acending_order = range(key_size - 1)
    decending_order = range(key_size - 1, 0, -1)
    rails = acending_order + decending_order

    # Find the position of each letter in the rails
    for position, letter in enumerate(cipher_text):
        fence[rails[position % len(rails)]][position] = letter

    if 0: # debug
        for rail in fence:
            print(''.join('.' if x is None else str(x) for x in rail))

    # If the entry is not none add it to the list to be returned
    return [x for rail in fence for x in rail if x is not None]

def encode(text, n):
    return ''.join(fence(text, n))

def decode(text, n):
    rng = range(len(text))
    pos = fence(rng, n)
    return ''.join(text[pos.index(n)] for n in rng)

# 10 chars dontattack
z = encode('DONTATTACKDONTATTACKDONTATTACKDONTATTACKDONTATTACKDONTATTACKDONTATTACKDONTATTACKDONTATTACK', 10)
# print(z) # ACTWTAKA.ANT.D

y = decode(z, 10 )
print(y) # ATTACK.AT.DAWN