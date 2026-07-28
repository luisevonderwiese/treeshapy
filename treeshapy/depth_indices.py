import math
import numpy as np

import treeshapy.util as util
from treeshapy.tree_index import TreeIndex

class SackinIndex(TreeIndex):
    #def evaluate_only(self, tree, mode):
    #    return sum(util.leaf_depths(tree))

    def evaluate(self, tree, mode):
        try:
            return tree.sackin_index
        except AttributeError:
            tree.add_feature("sackin_index", sum(util.leaf_depths(tree)))
            return tree.sackin_index

    def maximum(self, n, m, mode):
        return (n * m) - (((m - 1) * m) / 2)

    def minimum(self, n, m, mode):
        k = n - m + 1
        x = math.floor(math.log2(n / k))
        return (x + 3) * n - k * math.pow(2, x + 1)
    
    def exp_yule(self, n):
        return 2 * n * (util.H(n) - 1)
    
    def imbalance(self):
        return 1


class TotalPathLength(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.total_path_length
        except AttributeError:
            tree.add_feature("total_path_length", sum([util.depth(tree, node) for node in tree.traverse("postorder")]))
            return tree.total_path_length

    def maximum(self, n, m, mode):
        return (n * n) - n

    def minimum(self, n, m, mode):
        if n == 1:
            return 0
        if mode == "BINARY":
            log_val = math.floor(math.log2(n))
            return 2 * log_val * n - math.pow(2, log_val + 2) + 2 * n + 2
        if mode == "ARBITRARY":
            return n
    
    def exp_yule(self, n):
        return float("nan")
    
    def imbalance(self):
        return 1


class TotalInternalPathLength(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.total_internal_path_length
        except AttributeError:
            s = 0
            for node in tree.iter_descendants("postorder"):
                if not node.is_leaf():
                    s += util.depth(tree, node)
            tree.add_feature("total_internal_path_length", s)
            return tree.total_internal_path_length

    def maximum(self, n, m, mode):
        return ((n - 1) * (n - 2)) / 2

    def minimum(self, n, m, mode):
        if mode == "BINARY":
            log_val = math.floor(math.log2(n))
            return log_val * n - math.pow(2, log_val + 1) + 2
        if mode == "ARBITRARY":
            return 0
    
    def exp_yule(self, n):
        return float("nan")
    
    def imbalance(self):
        return 1


class AverageVertexDepth(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.average_vertex_depth
        except AttributeError:
            depths = [util.depth(tree, node) for node in tree.traverse("postorder")]
            tree.add_feature("average_vertex_depth", sum(depths) / len(depths))
            return tree.average_vertex_depth

    def maximum(self, n, m, mode):
        return ((n * n) - n) / (2 * n - 1)

    def minimum(self, n, m, mode):
        if n == 1:
            return 0
        if mode == "BINARY":
            log_val = math.floor(math.log2(n))
            return (2 * log_val * n - math.pow(2, log_val + 2) + 2 * n + 2) / (2 * n - 1)
        if mode == "ARBITRARY":
            return n / (n + 1)

    def exp_yule(self, n):
        return float("nan")
    
    def imbalance(self):
        return 1


class AverageLeafDepth(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.average_leaf_depth
        except AttributeError:
            depths = util.leaf_depths(tree)
            tree.add_feature("average_leaf_depth", sum(depths) / len(depths))
            return tree.average_leaf_depth

    def maximum(self, n, m, mode):
        return m - (((m - 1) * m) / (2 * n))

    def minimum(self, n, m, mode):
        k = n - m + 1
        x = math.floor(math.log2(n / k))
        return  x + 3 - (k / n) * math.pow(2, x + 1)

    def exp_yule(self, n):
        return 2 * util.H(n) - 2

    def imbalance(self):
        return 1


class VarianceOfLeavesDepths(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.variance_of_leaves_depths
        except AttributeError:
            tree.add_feature("variance_of_leaves_depths", float(np.var(util.leaf_depths(tree))))
            return tree.variance_of_leaves_depths

    def maximum(self, n, m, mode):
        return ((n - 1) * (n - 2) * (n*n + 3*n -6)) / (12 * n * n)

    def minimum(self, n, m, mode):
        if mode == "BINARY":
            return float("nan")
        if mode == "ARBITRARY":
            return 0

    def exp_yule(self, n):
        return ((2 * (n + 1)) / n) * util.H(n) + (1 / n) - 5

    def imbalance(self):
        return 1


class MaximumDepth(TreeIndex):
    #def evaluate_only(self, tree, mode):
    #    return max(util.leaf_depths(tree))

    def evaluate(self, tree, mode):
        try:
            return tree.maximum_depth
        except AttributeError:
            tree.add_feature("maximum_depth", max(util.leaf_depths(tree)))
            return tree.maximum_depth

    def maximum(self, n, m, mode):
        return n - 1

    def minimum(self, n, m, mode):
        if n == 1:
            return 0
        if mode == "BINARY":
            return math.ceil(math.log2(n))
        if mode == "ARBITRARY":
            return 1
    
    def exp_yule(self, n):
        return float("nan")
    
    def imbalance(self):
        return 1

class SShape(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.s_shape
        except AttributeError:
            s = 0
            for node in tree.traverse("postorder"):
                if not node.is_leaf():
                    s += math.log2(util.clade_size(tree, node) - 1)
            tree.add_feature("s_shape", s)
            return tree.s_shape

    def maximum(self, n, m, mode):
        return math.log2(math.factorial(n - 1))

    def minimum(self, n, m, mode):
        if mode == "BINARY":
            return float("nan")
        if mode == "ARBITRARY":
            if n == 1:
                return 0
            return math.log2(n - 1)

    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        return 1


class B1Index(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.B_1_index
        except AttributeError:
            s = 0
            try: #check if heights already precomputed
                tree.height
            except AttributeError:
                util.precompute_heights(tree)
            for node in tree.iter_descendants("postorder"):
                if node.is_leaf():
                    continue
                s += 1/ node.height
            tree.add_feature("B_1_index", s)
            return tree.B_1_index


    def maximum(self, n, m, mode):
        return float('nan')

    def minimum(self, n, m, mode):
        return float('nan')

    def exp_yule(self, n):
        return float("nan")
    
    def imbalance(self):
        return -1


class B2Index(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.B_2_index
        except AttributeError:
            s = 0
            try: #check if probs are already precomputed
                tree.prob
            except AttributeError:
                util.precompute_probs(tree)
            for leaf in tree.iter_leaves():
                p_leaf = leaf.prob
                try:
                    s += p_leaf * math.log2(p_leaf)
                except ValueError as e:
                    tree.add_feature("B_2_index", float("nan"))
                    return tree.B_2_index
            tree.add_feature("B_2_index", - s)
            return tree.B_2_index

    def maximum(self, n, m, mode):
        if mode == "BINARY":
            x  = math.floor(math.log2(n))
            pow_x = math.pow(2, x)
            return x + ((n - pow_x) / pow_x)
        if mode == "ARBITRARY":
            return math.log2(n)

    def minimum(self, n, m, mode):
        return 2 - math.pow(2, 2 - n)

    def exp_yule(self, n):
        return util.H(n - 1)

    def imbalance(self):
        return -1

