"""Sliding-window detection for repeated suspicious events within a time interval.

Uses a deque of timestamps per key so only events inside the current window
are counted. O(n) over the events for a full scan; O(1) amortised per event.
"""

from collections import deque


class SlidingWindowDetector:
    def __init__(self, window_seconds: int, threshold: int):
        if window_seconds <= 0 or threshold <= 0:
            raise ValueError("window_seconds and threshold must be positive")
        self.window_seconds = window_seconds
        self.threshold = threshold
        self._buckets: dict = {}  # key -> deque of timestamps

    def add_event(self, key, timestamp: float) -> bool:
        """Record an event; return True if threshold exceeded within window."""
        bucket = self._buckets.setdefault(key, deque())
        bucket.append(timestamp)
        # drop timestamps outside window (relative to newest)
        cutoff = timestamp - self.window_seconds
        while bucket and bucket[0] < cutoff:
            bucket.popleft()
        return len(bucket) >= self.threshold

    def count_in_window(self, key, now: float) -> int:
        bucket = self._buckets.get(key)
        if not bucket:
            return 0
        cutoff = now - self.window_seconds
        while bucket and bucket[0] < cutoff:
            bucket.popleft()
        return len(bucket)

    def reset(self, key=None) -> None:
        if key is None:
            self._buckets.clear()
        else:
            self._buckets.pop(key, None)
