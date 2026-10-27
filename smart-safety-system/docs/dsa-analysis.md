# DSA Analysis

| Component | File | Application | Time Complexity |
|---|---|---|---|
| EventQueue (FIFO) | app/dsa/event_queue.py | Process incoming events in order | enqueue O(1) amortized, dequeue O(1) amortized |
| CircularQueue | app/dsa/circular_queue.py | Recent events panel (fixed size) | enqueue/dequeue O(1), overflow O(1) |
| HashTable (separate chaining) | app/dsa/hash_table.py | Event type counts / fast lookup | insert/search/update/delete O(1) avg, O(n) worst |
| PriorityQueue (binary heap) | app/dsa/priority_queue.py | Prioritize by risk score/severity | enqueue/dequeue O(log n) |
| SlidingWindowDetector | app/dsa/sliding_window.py | Detect repeated suspicious events | O(1) amortized per event |
| Merge Sort | app/dsa/sorting.py | Sort event history | O(n log n) |
| Linear/Binary Search | app/dsa/searching.py | Event lookup | O(n) / O(log n) on sorted data |
| EventGraph | app/dsa/graph.py | Relate devices and events | BFS/DFS O(V+E) |
| Pattern Detection | app/dsa/pattern_detection.py | Rule-based sequence detection | O(n) |
