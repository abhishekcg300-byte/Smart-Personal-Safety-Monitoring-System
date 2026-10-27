"""Custom FIFO queue for processing incoming security events in order.

All operations are O(1) amortised using a dynamic array with a head pointer.
"""


class EventQueue:
    def __init__(self, initial_capacity: int = 16):
        self._data: list = []
        self._head: int = 0
        self._initial_capacity = initial_capacity

    def enqueue(self, item) -> None:
        """Insert at the rear. O(1) amortised."""
        self._data.append(item)

    def dequeue(self):
        """Remove and return the front element. O(1) amortised."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self._data[self._head]
        self._head += 1
        # reclaim memory periodically
        if self._head > 1024 and self._head > len(self._data) // 2:
            self._data = self._data[self._head:]
            self._head = 0
        return item

    def peek(self):
        """Return the front element without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._data[self._head]

    def is_empty(self) -> bool:
        return self._head >= len(self._data)

    def size(self) -> int:
        return len(self._data) - self._head

    def to_list(self) -> list:
        return list(self._data[self._head:])
