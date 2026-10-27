"""Binary-heap priority queue for security events.

Higher priority value is served first. Ties are broken by insertion order
(FIFO) using a monotonic counter, so behaviour is deterministic.
"""


class PriorityQueue:
    def __init__(self):
        self._heap: list = []   # each element: (-priority, counter, item)
        self._counter: int = 0

    def enqueue(self, item, priority: int) -> None:
        """Insert item with given priority. O(log n)."""
        entry = (-priority, self._counter, item)
        self._counter += 1
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)

    def dequeue(self):
        """Remove and return highest-priority item. O(log n)."""
        if self.is_empty():
            raise IndexError("dequeue from empty priority queue")
        top = self._heap[0][2]
        last = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            self._sift_down(0)
        return top

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty priority queue")
        return self._heap[0][2]

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)

    def to_list(self) -> list:
        # sorted copy by priority desc, tie by counter asc, without mutating
        sorted_heap = sorted(self._heap, key=lambda e: (e[0], e[1]))
        return [e[2] for e in sorted_heap]

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self._heap[idx][0] < self._heap[parent][0] or (
                self._heap[idx][0] == self._heap[parent][0]
                and self._heap[idx][1] < self._heap[parent][1]
            ):
                self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
                idx = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        n = len(self._heap)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx
            if left < n and (self._heap[left][0] < self._heap[smallest][0] or
                             (self._heap[left][0] == self._heap[smallest][0] and self._heap[left][1] < self._heap[smallest][1])):
                smallest = left
            if right < n and (self._heap[right][0] < self._heap[smallest][0] or
                              (self._heap[right][0] == self._heap[smallest][0] and self._heap[right][1] < self._heap[smallest][1])):
                smallest = right
            if smallest != idx:
                self._heap[idx], self._heap[smallest] = self._heap[smallest], self._heap[idx]
                idx = smallest
            else:
                break
