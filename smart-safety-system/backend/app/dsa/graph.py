"""Optional graph (adjacency list) for relating devices and events.

Supports BFS and DFS traversal. Relationships are only those the system
actually observes (e.g. events linked to a device); no fabricated connections.
"""


class EventGraph:
    def __init__(self):
        self._adj: dict = {}

    def add_node(self, node) -> None:
        self._adj.setdefault(node, [])

    def add_edge(self, a, b) -> None:
        self.add_node(a)
        self.add_node(b)
        if b not in self._adj[a]:
            self._adj[a].append(b)
        if a not in self._adj[b]:
            self._adj[b].append(a)

    def bfs(self, start) -> list:
        if start not in self._adj:
            return []
        visited = {start}
        q = [start]
        out = []
        while q:
            node = q.pop(0)
            out.append(node)
            for nb in self._adj.get(node, []):
                if nb not in visited:
                    visited.add(nb)
                    q.append(nb)
        return out

    def dfs(self, start) -> list:
        if start not in self._adj:
            return []
        visited = set()
        out = []

        def _dfs(node):
            if node in visited:
                return
            visited.add(node)
            out.append(node)
            for nb in self._adj.get(node, []):
                _dfs(nb)

        _dfs(start)
        return out

    def neighbors(self, node) -> list:
        return list(self._adj.get(node, []))
