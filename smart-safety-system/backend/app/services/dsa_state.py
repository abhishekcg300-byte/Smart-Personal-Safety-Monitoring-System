"""In-memory DSA state used by the event-processing pipeline and the demo page."""

from app.dsa.event_queue import EventQueue
from app.dsa.circular_queue import CircularQueue
from app.dsa.hash_table import HashTable
from app.dsa.priority_queue import PriorityQueue
from app.dsa.sliding_window import SlidingWindowDetector

_STATE = {}


def get_state(device_id: int) -> dict:
    if device_id not in _STATE:
        _STATE[device_id] = {
            "fifo": EventQueue(),
            "recent": CircularQueue(20),
            "type_counts": HashTable(),
            "priority": PriorityQueue(),
            "sliding": SlidingWindowDetector(window_seconds=300, threshold=5),
        }
    return _STATE[device_id]


def global_counts() -> HashTable:
    if "_global" not in _STATE:
        _STATE["_global"] = HashTable()
    return _STATE["_global"]
