
def parse_file(file, strings):

    with open(file) as f:
        strings += f.read()

    words = strings.split('\n')

    return ' '.join(words)

def main():
    file = '/Users/kateharline/Desktop/rosalind_mprt.txt'
    strings = ''

    parse = parse_file(file, strings)

    return parse.split(' ')

if __name__ == '__main__':
    main()