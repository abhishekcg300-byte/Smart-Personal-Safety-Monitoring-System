import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.dsa.event_queue import EventQueue
from app.dsa.circular_queue import CircularQueue
from app.dsa.hash_table import HashTable
from app.dsa.priority_queue import PriorityQueue
from app.dsa.sliding_window import SlidingWindowDetector
from app.dsa.sorting import merge_sort
from app.dsa.searching import linear_search, binary_search
from app.dsa.graph import EventGraph
from app.dsa.pattern_detection import detect_patterns

def test_queue():
    q = EventQueue()
    assert q.is_empty()
    q.enqueue(1); q.enqueue(2)
    assert q.size() == 2
    assert q.peek() == 1
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.is_empty()

def test_circular_overflow():
    c = CircularQueue(3)
    for i in range(5):
        c.enqueue(i)
    assert c.size() == 3
    assert c.to_list() == [2,3,4]

def test_hash_table_collision():
    h = HashTable(initial_capacity=2)
    h.insert("a", 1)
    h.insert("b", 2)
    h.insert("c", 3)
    assert h.search("a") == 1
    assert h.search("b") == 2
    assert h.search("c") == 3
    assert h.update("a", 9)
    assert h.search("a") == 9
    assert h.delete("b") is True
    assert h.search("b") is None

def test_heap_ordering():
    pq = PriorityQueue()
    pq.enqueue("low", 1)
    pq.enqueue("critical", 10)
    pq.enqueue("mid", 5)
    assert pq.dequeue() == "critical"
    assert pq.dequeue() == "mid"
    assert pq.dequeue() == "low"

def test_sliding_window_boundary():
    sw = SlidingWindowDetector(window_seconds=10, threshold=3)
    assert sw.add_event("k", 0) is False
    assert sw.add_event("k", 5) is False
    assert sw.add_event("k", 9) is True
    # outside window
    sw2 = SlidingWindowDetector(window_seconds=10, threshold=2)
    sw2.add_event("k", 0)
    assert sw2.add_event("k", 100) is False

def test_merge_sort():
    data = [5,3,8,1,9,2]
    assert merge_sort(data) == sorted(data)
    assert merge_sort(data, key=lambda x: -x) == sorted(data, reverse=True)

def test_searching():
    arr = [1,2,3,4,5]
    assert linear_search(arr, lambda x: x > 3) == [4,5]
    assert binary_search(arr, 3) == 2
    assert binary_search(arr, 99) == -1

def test_graph():
    g = EventGraph()
    g.add_edge("dev1", "evt1")
    g.add_edge("evt1", "evt2")
    assert "evt2" in g.bfs("dev1")
    assert "dev1" in g.dfs("evt2")

def test_pattern_detection():
    evs = [{"event_type": "APP_LOGIN_FAILED"}, {"event_type": "APP_LOGIN_FAILED"},
           {"event_type": "APP_LOGIN_FAILED"}, {"event_type": "HEARTBEAT_MISSED"},
           {"event_type": "SUSPICIOUS_APP_ACCESS"}]
    p = detect_patterns(evs)
    assert "repeated_app_login_failures" in p
    assert "high_risk_compound" in p
