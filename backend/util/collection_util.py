def minus_dict(a, b):
    al = len(a)
    bl = len(b)
    for i in reversed(range(al)):
        for j in range(bl):
            if a[i] == b[j]:
                del a[i]


def unique_dict(original):
    le = len(original)
    for i in reversed(range(le)):
        for j in reversed(range(i)):
            if original[i] == original[j]:
                del original[i]
                break