import collections


def minus_dict(a, b):
    al = len(a)
    bl = len(b)
    for i in reversed(range(al)):
        for j in reversed(range(bl)):
            if a[i] == b[j]:
                del a[i]
                break


def unique_dict(original):
    le = len(original)
    for i in reversed(range(le)):
        for j in reversed(range(i)):
            if original[i] == original[j]:
                del original[i]
                break


def sort_dict(dict, f):
    return collections.OrderedDict(sorted(dict.items(), key=f))


if __name__ == '__main__':
    # unique_dict([{'x': 1, 'y': 2}, {'x': 1, 'y': 2}, {'x': 2, 'y': 2}])
    y_ = [{'x': 1, 'y': 2}, {'x': 2, 'y': 2}, {'x':3, 'y':3},{'x':4,'y':5}]
    minus_dict(y_, [{'x': 2, 'y': 2}, {'x':3, 'y':3},{'x':4,'y':5}])
    print(y_)
    # sort_by_time({1: {'time': 1}, 2: {'time': 4}, 3: {'time': 3}}, lambda args: args[1]['time'])
