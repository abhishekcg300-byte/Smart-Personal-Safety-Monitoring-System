"""Searching utilities: linear search and binary search (sorted data only)."""


def linear_search(items: list, predicate) -> list:
    """Return all items where predicate(item) is True. O(n)."""
    return [x for x in items if predicate(x)]


def binary_search(sorted_items: list, key, key_func=None) -> int:
    """Return index of key in sorted_items, or -1. Requires sorted input. O(log n)."""
    if key_func is None:
        key_func = lambda x: x
    lo, hi = 0, len(sorted_items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = key_func(sorted_items[mid])
        if val == key:
            return mid
        if val < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
