def iter_chunks(iterator, k=10):
    i = 0
    x = []
    for el in iterator:
        i += 1
        x.append(el)
        if i==k:
            yield x
            x = []
            i = 0
    if x:
        yield x
