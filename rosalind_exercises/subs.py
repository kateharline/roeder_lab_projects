import sys

def subs(string, substring):
    length = len(substring)

    pos = []

    for i in range(0, len(string)-length):

        print(string[i:i+length].split())
        print(substring)
        if string[i:i+length].split() == substring:
            pos.append(i+1)

    return ' '.join(map(str, pos))
