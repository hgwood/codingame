from itertools import islice, takewhile

def conway_compress(phrase):
    if not phrase: return tuple()
    first = phrase[0]
    length = len(tuple(takewhile(lambda value: value == first, phrase)))
    return (length, first) + conway_compress(phrase[length:])

def conway(root):
    phrase = root
    while True:
        yield phrase
        phrase = conway_compress(phrase)

if __name__ == "__main__":
    root = (int(input()),)
    nconway = int(input())
    nth_conway = next(islice(conway(root), nconway - 1, nconway))
    print(" ".join(map(str, nth_conway)))
