from packages.analyse import WordBuilder
from packages.pad import Decode
import itertools


m = ['W', 'U', 'M', 'C', 'F']
n = ['A', 'O', 'N', 'I', 'H']
# u = ['D', 'L', 'U', 'W', 'M']
u = ['M']
t = ['A', 'T', 'E']
f = ['M', 'C', 'F', 'G', 'H']
# t is next




# possible_words = ['FILE',]
# word_builder = WordBuilder(possible_words)
# word_builder.run()

print(4)
possible_words = itertools.product(m,n,u,t)
word_builder = WordBuilder(possible_words)
word_builder.run()
print(5)

possible_words = itertools.product(m,n,u,t,f)
word_builder = WordBuilder(possible_words)
word_builder.run()

print(6)
possible_words = itertools.product(m,n,u,t,f,t)
word_builder = WordBuilder(possible_words)
word_builder.run()