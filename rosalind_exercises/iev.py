import sys

couple_probs = [1.0, 1.0, 1.0, .75, .5, 0 ]
couples = sys.argv[1:]

# convert to ints
couple_ints = list(map(int, couples))

e = 0

for i, int in enumerate(couple_ints):
    e += 2 * int * couple_probs[i]

print(e)