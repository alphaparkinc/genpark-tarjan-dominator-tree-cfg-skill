from client import DominatorTree

cfg = DominatorTree(4)
cfg.add_edge(0, 1)
cfg.add_edge(0, 2)
cfg.add_edge(1, 3)
cfg.add_edge(2, 3)

dom, idom = cfg.compute_dominators(root=0)
print("Dominator sets:", dom)
print("Immediate dominators (idom):", idom)
