"""Merge Sort implementation for historical event ordering."""


def merge_sort(items: list, key=None, reverse: bool = False) -> list:
    """Return a new sorted list using merge sort. O(n log n)."""
    if key is None:
        key = lambda x: x
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    left = merge_sort(items[:mid], key, reverse)
    right = merge_sort(items[mid:], key, reverse)
    merged = _merge(left, right, key, reverse)
    return merged


def _merge(left, right, key, reverse):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        li = key(left[i])
        rj = key(right[j])
        if (li <= rj) ^ reverse:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
