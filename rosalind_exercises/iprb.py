import sys

k, m, n = sys.argv[1:]

def problem(k, m, n):
    k, m, n = map(float, (k, m, n))
    p = [
        k * (k - 1),  # AA, AA pairs
        k * m,  # AA, Aa pairs
        k * n,  # AA, aa pairs
        m * k,  # Aa, AA pairs
        m * (m - 1) * 0.75, # Aa, Aa pairs
        m * n * 0.5, # Aa, aa pairs
        n * k,  # aa, AA pairs
        n * m * 0.5,  # aa, Aa pairs
        0,  # aa, aa pairs
    ]
    t = k + m + n
    return sum(p) / t / (t - 1)

mendel = round(problem(k, m, n), 5)

print(mendel)