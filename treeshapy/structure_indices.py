import math
from collections import Counter

import treeshapy.util as util
from treeshapy.tree_index import TreeIndex


class DIndex(TreeIndex):
    def evaluate(self, tree, binary):
        try:
            return tree.d_index
        except AttributeError:
            n = util.clade_size(tree, tree)
            if n == 1:
                tree.add_feature("d_index", 0)
            else:
                f_n = Counter([util.clade_size(tree, node) for node in tree.traverse()])
                num_inner_nodes = len([_ for _ in tree.traverse()]) - n
                s = 0
                for z in range(2, n):
                    p_n = (n / (n - 1)) * (2 / (z * (z + 1)))
                    s += z * abs(f_n[z] / num_inner_nodes - p_n)
                s += n * abs(f_n[n] / num_inner_nodes - (1 / (n - 1)))
                tree.add_feature("d_index", s)
            return tree.d_index

    def maximum(self, n, m, binary):
        return float("nan")

    def minimum(self, n, m, binary):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")


class RootedQuartetIndex(TreeIndex):
    def evaluate(self, tree, binary):
        try:
            return tree.rooted_quartet_index #check if rqis already precomputed
        except AttributeError:
            util.precompute_rqi(tree)
            return tree.rooted_quartet_index

    def maximum(self, n, m, binary):
        if binary:
            return float("nan")
        else:
            return 4 * math.comb(n, 4)

    def minimum(self, n, m, binary):
        return 0

    def exp_yule(self, n):
        return math.comb(n, 4) 


class AverageLadder(TreeIndex):
    def evaluate(self, tree, binary):
        if not binary:
            raise ValueError("average_ladder is not defined for arbitrary trees")
        try:
            return tree.average_ladder
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("average_ladder", 0)
                return tree.average_ladder
            try:
                tree.ladder_length
            except AttributeError:
                util.precompute_ladder_lengths(tree)
            l = [node.ladder_length for node in tree.traverse() if node.ladder_length > 0]
            if len(l) == 0:
                tree.add_feature("average_ladder", 0)
            else:
                tree.add_feature("average_ladder", sum(l) / len(l))
            return tree.average_ladder

    def maximum(self, n, m, binary):
        return float("nan")

    def minimum(self, n, m, binary):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

class LadderLength(TreeIndex):
    def evaluate(self, tree, binary):
        if not binary:
            raise ValueError("ladder_length is not defined for arbitrary trees")
        try:
            return tree.max_ladder_length
        except AttributeError:
            try:
                tree.max_ladder_length
            except AttributeError:
                util.precompute_ladder_lengths(tree)
            tree.add_feature("max_ladder_length", max([node.ladder_length for node in tree.traverse()]))
            return tree.max_ladder_length

    def maximum(self, n, m, binary):
        return float("nan")

    def minimum(self, n, m, binary):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

