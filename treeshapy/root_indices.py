import math

import treeshapy.util as util
from treeshapy.tree_index import TreeIndex

class RootImbalance(TreeIndex):
    def evaluate(self, tree, mode):
        if mode == "ARBITRARY":
            raise ValueError("root_imbalance is not defined for arbitrary trees")
        try:
            return tree.root_imbalance
        except AttributeError:
            if tree.is_leaf(): #single-node-tree
                tree.add_feature("root_imbalance", 0)
            else:
                c = tree.children
                assert (len(c) == 2)
                tree.add_feature("root_imbalance", max(util.clade_size(tree, c[0]), util.clade_size(tree, c[1])) / util.clade_size(tree, tree))
            return tree.root_imbalance

    def maximum(self, n, m, mode):
        if mode == "BINARY":
            return (n - 1) / n
        if mode == "ARBITRARY":
            return float("nan")

    def minimum(self, n, m, mode):
        if mode == "BINARY":
            if n == 1:
                return 0
            return math.ceil(n / 2) / n
        if mode == "ARBITRARY":
            return float("nan")

    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        return 0


class IRoot(TreeIndex):
    def evaluate(self, tree, mode):
        if mode == "ARBITRARY":
            raise ValueError("I_root is not defined for arbitrary trees")
        try:
            return tree.I_root
        except AttributeError:
            if tree.is_leaf(): #single-node-tree
                tree.add_feature("I_root", 0)
            else:
                tree.add_feature("I_root", util.I_value(tree, tree))
            return tree.I_root

    def maximum(self, n, m, mode):
        if mode == "BINARY":
            if n == 1:
                return 0
            return 1
        if mode == "ARBITRARY":
            return float("nan")

    def minimum(self, n, m, mode):
        if mode == "BINARY":
            return 0
        if mode == "ARBITRARY":
            return float("nan")

    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        return 0
