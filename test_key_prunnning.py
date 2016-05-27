from kasiski import Kasiski
from itertools import product, combinations_with_replacement, permutations, combinations
class decode:
    def __init__(self, key):
        self.key = key
        self.multiples_list = Kasiski(self.key).multiples_list
        self.multiples_list.remove(len(key))
        print(self.multiples_list)

    def prune_keys(self):
        key = self.key
        key = ''.join(key)
        len_key = len(key)

        for each_completed_keysize in self.multiples_list:
            break_up_key_size = int(len_key / each_completed_keysize)
            print(break_up_key_size)
            x = [key[i:i+each_completed_keysize] for i in range(0, len_key, each_completed_keysize)]
            # print(x)
            if self.check_if_all_equal(x) is True:
                    print(each_completed_keysize)
                    print(x)
                    print('Prunning: %s' % str(key))
                    return True
            else:
                print('not prunning: %s:%s' % (str(key), str(x)))
        return False

    def check_if_all_equal(self, iterator):
        try:
            iterator = iter(iterator)
            first = next(iterator)
            return all(first == rest for rest in iterator)
        except StopIteration:
            return True

#
# one = decode('abc')
# one.prune_keys()
# print('*'*20)
# two = decode('aaaa')
# two.prune_keys()
# print('*'*20)
# three = decode('abab')
# three.prune_keys()
# print('*'*20)
# four = decode('aabbccdd')
# four.prune_keys()


def combinations_with_replacement_with_prunning(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    for indices in product(range(n), repeat=r):
        if sorted(indices) == list(indices):
            output = tuple(pool[i] for i in indices)

            if decode(''.join(output)).prune_keys() is False:
                yield output

def product_with_prunning(*args, repeat=1):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        output = tuple(prod)
        if decode(''.join(output)).prune_keys() is False:
            yield output

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z']
derp = product_with_prunning(''.join(alphabet), repeat=4)

for each in derp:
    print(each)