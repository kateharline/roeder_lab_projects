import sys

k, N = list(map(int, sys.argv[1:]))

def binomial(n, k):
    """Compute n factorial by a direct multiplicative method."""
    if k > n - k:
        k = n - k  # Use symmetry of Pascal's triangle
    accum = 1
    for i in range(1, k + 1):
        accum *= (n - (k - i))
        accum /= i
    return accum

def P(n, k):
    '''probability of exactly n hets at level k'''
    return binomial(2 ** k, n) * 0.25 ** n * 0.75 ** (2 ** k - n)

print(1 - sum([P(n, k) for n in range(N)]))