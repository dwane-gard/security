from packages.analyse import WordBuilder
from packages.pad import Decode
import itertools

alpha = [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']

m = ['W', 'U', 'M', 'C', 'F']
n = ['A', 'O', 'N', 'I', 'H']
#
# U = ['M']
t = ['A', 'T', 'E', 'O']
f = ['M', 'C', 'F', 'G', 'H']
# t is next
u = ['D', 'L', 'U', 'W', 'M']
# t
d = ['D', 'L', 'R' 'S', 'U']
e = ['A', 'T', 'E']
h = ['N','I', 'H','S', 'R']
y = ['F', 'G', 'Y', 'P', 'B']
a= ['A', 'T', 'O', 'N']


possible_words = itertools.product('mathematic',alpha, alpha,alpha)
word_builder = WordBuilder(possible_words)
word_builder.run_equal()
word_builder.run_in()
# possible_words = ['FILE',]
# word_builder = WordBuilder(possible_words)
# word_builder.run()

# print(4)
possible_words = itertools.product(m,n,m,t,f,t)
word_builder = WordBuilder(possible_words)
word_builder.run_equal()
# # word_builder.run_in()
# print(5)
#
# possible_words = itertools.product(m,n,u,t,f)
# word_builder = WordBuilder(possible_words)
# word_builder.run_equal()
# word_builder.run_in()

# print(6)
# possible_words = itertools.product(m,n,u,t,f,t)
# word_builder = WordBuilder(possible_words)
# # word_builder.run_equal()
# word_builder.run_in()
#
# print(7)
# possible_words = itertools.product(m,n,u,t,f,t, u)
# word_builder = WordBuilder(possible_words)
# # word_builder.run_equal()
# word_builder.run_in()
#
# print(8)
# possible_words = itertools.product(m,n,u,t,f,t,u,t)
# word_builder = WordBuilder(possible_words)
# # word_builder.run_equal()
# word_builder.run_in()
