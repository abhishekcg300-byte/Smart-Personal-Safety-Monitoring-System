"""Fixed-size circular queue (ring buffer) for the recent-events panel.

Policy when full: overwrite the oldest element (FIFO eviction). This keeps the
most recent N events available for the dashboard.
"""


class CircularQueue:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._buf: list = [None] * capacity
        self._head: int = 0  # next slot to write
        self._size: int = 0

    def enqueue(self, item) -> None:
        """Insert item; overwrites oldest when full. O(1)."""
        self._buf[self._head] = item
        self._head = (self._head + 1) % self.capacity
        if self._size < self.capacity:
            self._size += 1

    def dequeue(self):
        """Remove and return the oldest element. O(1)."""
        if self.is_empty():
            raise IndexError("dequeue from empty circular queue")
        # oldest is the slot just after the most recent write window
        oldest_idx = (self._head - self._size) % self.capacity
        item = self._buf[oldest_idx]
        self._buf[oldest_idx] = None
        self._size -= 1
        return item

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty circular queue")
        oldest_idx = (self._head - self._size) % self.capacity
        return self._buf[oldest_idx]

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self.capacity

    def size(self) -> int:
        return self._size

    def to_list(self) -> list:
        out = []
        for i in range(self._size):
            idx = (self._head - self._size + i) % self.capacity
            out.append(self._buf[idx])
        return out
