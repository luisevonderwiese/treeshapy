import os
from ete3 import Tree
from copy import deepcopy
from treeshapy import TreeShape

def _all_rooted_trees(tree):
    internal_count = 0
    node_names = []
    for node in tree.iter_descendants():
        if not node.is_leaf():
            node.name = "internal_" + str(internal_count)
            internal_count += 1
        node_names.append(node.name)
    rooted_trees = {}
    for name in node_names:
        rooted_tree = deepcopy(tree)
        root = rooted_tree&name
        rooted_tree.set_outgroup(root)
        rooted_trees[name] = rooted_tree
    return rooted_trees


class AllRootTreeShape:
    def __init__(self, tree, mode, rooted = True):
        self.all_rooted_trees = _all_rooted_trees(tree)
        self.ts_instances = {name : TreeShape(tree, mode, rooted) for name, tree in self.all_rooted_trees.items()}

    def absolute(self, index_name):
        return {name : ts.absolute(index_name) for name, ts in self.ts_instances.items()}

    def relative(self, index_name, rel):
        return {name : ts.relative(index_name, rel) for name, ts in self.ts_instances.items()}

    def all_absolute(self):
        return {name : ts.all_absolute() for name, ts in self.ts_instances.items()}

    def all_relative(self, rel):
        return {name : ts.all_relative(rel) for name, ts in self.ts_instances.items()}

    def subset_absolute(self, k):
        return {name : ts.subset_absolute(k) for name, ts in self.ts_instances.items()}

    def subset_relative(self, rel, k):
        return {name : ts.subset_relative(rel, k) for name, ts in self.ts_instances.items()}


