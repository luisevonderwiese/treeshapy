from ete3 import Tree

import treeshapy
from treeshapy import TreeShape

treeshapy.INDICES

t = Tree("example_rooted.tree")
ts = TreeShape(t)
ts.index_list()
ts.index_list("REL_MAX")
ts.index_list(10)

c = ts.evaluate("colless_index")
c_rel = ts.evaluate("colless_index", "REL_TIPS")

ts.evaluate("all")
ts.evaluate("all", "REL_TIPS")

ts.evaluate(10)

t = Tree("example_unrooted.tree")
ts = TreeShape(t)
ts.index_list("ABS")
ts.get_all_rooted_trees()

ts.evaluate("all")
ts.evaluate_for_all_roots("colless_index")
ts.evaluate_for_all_roots("all")



