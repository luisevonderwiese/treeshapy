from ete3 import Tree

import treeshapy
from treeshapy import TreeShape

#list of all implemented indices
print(treeshapy.INDICES)

t = Tree("example_rooted.tree")
# "binary" and "rooted" flags are set depending on the trees properties
ts = TreeShape(t)
print(ts.index_list("ABS"))
print(ts.index_list("REL_MAX"))
print(ts.index_list(10))

c = ts.evaluate("colless_index")
c_rel = ts.evaluate("colless_index", "REL_TIPS")

res = ts.evaluate("all")
c = res["colless_index"]
res = ts.evaluate("all", "REL_TIPS")
c_rel = res["colless_index"]

res = ts.evaluate(10)
print(res)

t = Tree("example_unrooted.tree")
# "binary" and "rooted" flags are set depending on the trees properties
ts = TreeShape(t)
print(ts.index_list("ABS"))

print(ts.evaluate("all"))

res = ts.evaluate_for_all_roots("colless_index")
c = res["internal_0"]

res = ts.evaluate_for_all_roots("all")
c = res["internal_0"]["colless_index"]



