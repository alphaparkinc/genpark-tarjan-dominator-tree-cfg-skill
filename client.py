"""Dominator Tree and Immediate Dominators Engine.
100% Python Standard Library.
"""

import collections

class DominatorTree:
    """Computes immediate dominators (idom) on directed control flow graphs."""
    def __init__(self, num_nodes):
        self.n = num_nodes
        self.adj = collections.defaultdict(list)
        self.pred = collections.defaultdict(list)

    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.pred[v].append(u)

    def compute_dominators(self, root=0):
        dom = {}
        all_nodes = set(range(self.n))
        for i in range(self.n):
            dom[i] = {root} if i == root else set(all_nodes)

        changed = True
        while changed:
            changed = False
            for u in range(self.n):
                if u == root:
                    continue
                if self.pred[u]:
                    new_dom = set.intersection(*(dom[p] for p in self.pred[u])) | {u}
                else:
                    new_dom = {u}
                if new_dom != dom[u]:
                    dom[u] = new_dom
                    changed = True

        idom = {}
        for u in range(self.n):
            if u == root:
                idom[u] = None
                continue
            strict_doms = dom[u] - {u}
            for d in strict_doms:
                if dom[d] == strict_doms:
                    idom[u] = d
                    break
        return dom, idom
