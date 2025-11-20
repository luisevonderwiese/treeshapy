import numpy as np

import treeshapy.util as util
from treeshapy.tree_index import TreeIndex

class Treeness(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.treeness
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("treeness", 0)
            else:
                all_brlens = 0
                internal_brlens = 0
                for node in tree.traverse("postorder"):
                    brlen = node.dist
                    all_brlens += brlen
                    if not node.is_leaf():
                        internal_brlens += brlen
                tree.add_feature("treeness", internal_brlens / all_brlens)
            return tree.treeness

    def maximum(self, n, m, mode):
        if n == 1:
            return 0
        return 1 #pseudo bound

    def minimum(self, n, m, mode):
        return 0

    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        return 0


class Stemminess(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.stemminess
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("stemminess", 0)
            else:
                values = []
                for node in tree.iter_descendants("postorder"):
                    d = node.dist
                    if node.is_leaf():
                        node.add_feature("sum_below", d)
                    else:
                        c = node.children
                        s = d + sum([child.sum_below for child in c])
                        node.add_feature("sum_below", s)
                        if s == 0:
                            continue
                        values.append(d / s)
                tree.add_feature("stemminess", sum(values) / len(values))
            return tree.stemminess

    def maximum(self, n, m, mode):
        if n == 1:
            return 0
        return 1 #pseudo bound

    def minimum(self, n, m, mode):
        return 0

    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        return 0



