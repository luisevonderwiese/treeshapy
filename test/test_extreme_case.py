from ete3 import Tree
from treeshapy import TreeShape, INDICES

tree =  Tree("A;")
ts = TreeShape(tree, "BINARY")
ts.evaluate("all")
ts.evaluate("all", "REL_TIPS")
ts.evaluate("all", "REL_MAX")
ts.evaluate("all", "REL_YULE")
ts = TreeShape(tree, "ARBITRARY")
ts.evaluate("all")
ts.evaluate("all", "REL_TIPS")
ts.evaluate("all", "REL_MAX")


