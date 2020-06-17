def jaccard(reference: list, candidate: list) -> float:
    """Provide an evaluation metric."""
    a = set(reference)
    b = set(candidate)
    c = a.intersection(b)
    try:
        res = float(len(c)) / (len(a) + len(b) - len(c))
    except ZeroDivisionError:
        return 0
    return res
