"""Custom hash table using separate chaining for collision resolution.

Used for fast lookup/counting of event IDs, event types and device statistics.
"""


class HashTable:
    def __init__(self, initial_capacity: int = 16, load_factor: float = 0.75):
        self._capacity = max(1, initial_capacity)
        self._load_factor = load_factor
        self._size = 0
        self._buckets: list = [[] for _ in range(self._capacity)]

    def _hash(self, key) -> int:
        # deterministic polynomial rolling hash
        h = 0
        for ch in str(key):
            h = (h * 31 + ord(ch)) & 0xFFFFFFFF
        return h % self._capacity

    def _resize(self) -> None:
        old = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for bucket in old:
            for k, v in bucket:
                self.insert(k, v)

    def insert(self, key, value) -> None:
        """Insert or overwrite value for key. O(1) average."""
        if self._size / self._capacity >= self._load_factor:
            self._resize()
        idx = self._hash(key)
        for i, (k, _) in enumerate(self._buckets[idx]):
            if k == key:
                self._buckets[idx][i] = (key, value)
                return
        self._buckets[idx].append((key, value))
        self._size += 1

    def search(self, key):
        """Return value if present else None. O(1) average."""
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return None

    def contains(self, key) -> bool:
        return self.search(key) is not None or any(k == key for k, _ in self._buckets[self._hash(key)])

    def delete(self, key) -> bool:
        idx = self._hash(key)
        for i, (k, _) in enumerate(self._buckets[idx]):
            if k == key:
                del self._buckets[idx][i]
                self._size -= 1
                return True
        return False

    def update(self, key, value) -> bool:
        idx = self._hash(key)
        for i, (k, _) in enumerate(self._buckets[idx]):
            if k == key:
                self._buckets[idx][i] = (key, value)
                return True
        return False

    def keys(self) -> list:
        out = []
        for bucket in self._buckets:
            for k, _ in bucket:
                out.append(k)
        return out

    def items(self) -> list:
        out = []
        for bucket in self._buckets:
            for k, v in bucket:
                out.append((k, v))
        return out

    def size(self) -> int:
        return self._size
