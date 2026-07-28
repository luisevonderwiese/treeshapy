import math

import treeshapy.util as util
from treeshapy.tree_index import TreeIndex

class CollessIndex(TreeIndex):
    #def evaluate_only(self, tree, mode):
    #    s = 0
    #    for node in tree.traverse("postorder"):
    #        if not node.is_leaf():
    #            s += util.balance_index(tree, node)
    #    return s

    def evaluate(self, tree, mode):
        if mode == "ARBITRARY":
            raise ValueError("colless_index is not defined for arbitrary trees")
        try:
            return tree.colless_index
        except AttributeError:
            s = 0
            for node in tree.traverse("postorder"):
                if not node.is_leaf():
                    s += util.balance_index(tree, node)
            tree.add_feature("colless_index", s)
            return tree.colless_index

    def maximum(self, n, m, mode):
        if mode == "BINARY":
            return ((n - 1) * (n - 2)) / 2
        if mode == "ARBITRARY":
            return float("nan")

    def minimum(self, n, m, mode):
        if mode == "BINARY":
            sum_bound = math.ceil(math.log2(n))
            s = 0
            for j in range(1, sum_bound):
                x = math.pow(2, -j) * n
                triangle_wave = min(math.ceil(x) - x, x - math.floor(x))
                s += math.pow(2, j) * triangle_wave
            return s
        if mode == "ARBITRARY":
            return float("nan")

    def exp_yule(self, n):
        return (n % 2) + n * (util.H(math.floor(n / 2)) - 1)

    def imbalance(self):
        return 1


class CorrectedCollessIndex(TreeIndex):
    def evaluate(self, tree, mode):
        if mode == "ARBITRARY":
            raise ValueError("corrected_colless_index is not defined for arbitrary trees")
        try:
            return tree.corrected_colless_index
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("corrected_colless_index", 0)
            else:
                n = util.clade_size(tree, tree)
                tree.add_feature("corrected_colless_index", (2 * CollessIndex().evaluate(tree, mode)) / ((n-1) * (n-2)))
            return tree.corrected_colless_index

    def maximum(self, n, m, mode):
        if mode == "BINARY":
            if n <= 2:
                return 0
            return 1
        if mode == "ARBITRARY":
            return float("nan")

    def minimum(self, n, m, mode):
        if mode == "BINARY":
            if n <= 2:
                return 0
            return (2 / ((n - 1) * (n - 2))) * CollessIndex().minimum(n, m, mode)
        if mode == "ARBITRARY":
            return float("nan")

    def exp_yule(self, n):
        e_colless = (n % 2) + n * (util.H(math.floor(n / 2)) - 1)
        return (2 * e_colless) / ((n - 1) * (n - 2))
    
    def imbalance(self):
        return 1


class QuadraticCollessIndex(TreeIndex):
    def evaluate(self, tree, mode):
        if mode == "ARBITRARY":
            raise ValueError("quadratic_colless_index is not defined for arbitrary trees")
        try:
            return tree.quadratic_colless_index
        except AttributeError:
            s = 0
            for node in tree.traverse("postorder"):
                if not node.is_leaf():
                    b = util.balance_index(tree, node)
                    s += b * b
            tree.add_feature("quadratic_colless_index", s)
            return tree.quadratic_colless_index

    def maximum(self, n, m, mode):
        if mode == "BINARY":
            return math.comb(n, 3) + math.comb(n - 1, 3)
        if mode == "ARBITRARY":
            return float("nan")

    def minimum(self, n, m, mode):
        if mode == "BINARY":
            sum_bound = math.ceil(math.log2(n))
            s = 0
            for j in range(1, sum_bound):
                x = math.pow(2, -j) * n
                triangle_wave = min(math.ceil(x) - x, x - math.floor(x))
                s += math.pow(2, j) * triangle_wave
            return s
        if mode == "ARBITRARY":
            return float("nan")
    
    def exp_yule(self, n):
        return n * (n + 1) - 2 * n * util.H(n)
    
    def imbalance(self):
        return 1


class I2Index(TreeIndex):
    def evaluate(self, tree, mode):
        if mode == "ARBITRARY":
            raise ValueError("I_2_index is not defined for arbitrary trees")
        try:
            return tree.I_2_index
        except AttributeError:
            n = util.clade_size(tree, tree)
            if n <= 2:
                tree.add_feature("I_2_index", 0)
            else:
                s = 0
                for node in tree.traverse("postorder"):
                    n_v = util.clade_size(tree, node)
                    if n_v > 2:
                        b = util.balance_index(tree, node)
                        s += b / (n_v - 2)
                tree.add_feature("I_2_index", s / (n - 2))
            return tree.I_2_index

    def maximum(self, n, m, mode):
        if mode == "BINARY":
            if n <= 2:
                return 0
            return 1
        if mode == "ARBITRARY":
            return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        return 1


class Stairs1(TreeIndex):
    def evaluate(self, tree, mode):
        if mode == "ARBITRARY":
            raise ValueError("stairs1 is not defined for arbitrary trees")
        try:
            return tree.stairs1
        except AttributeError:
            if tree.is_leaf():
                return tree.add_feature("stairs1", 0)
            else:
                tree.add_feature("stairs1", RogersJIndex().evaluate(tree, mode) /  (util.clade_size(tree, tree)- 1))
            return tree.stairs1

    def maximum(self, n, m, mode):
        if mode == "BINARY":
            if n == 1:
                return 0
            return (n - 2) / (n - 1)
        if mode == "ARBITRARY":
            return float("nan")

    def minimum(self, n, m, mode):
        if mode == "BINARY":
            if n == 1:
                return 0
            return (bin(n).count("1") - 1) / (n - 1)
        if mode == "ARBITRARY":
            return float("nan")

    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        raise 1


class Stairs2(TreeIndex):
    def evaluate(self, tree, mode):
        if mode == "ARBITRARY":
            raise ValueError("stairs2 is not defined for arbitrary trees")
        try:
            return tree.stairs2
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("stairs2", 0)
            else:
                s = 0
                for node in tree.traverse("postorder"):
                    if node.is_leaf():
                        continue
                    c = node.children
                    assert (len(c) == 2)
                    n0 = util.clade_size(tree, c[0])
                    n1 = util.clade_size(tree, c[1])
                    s += min(n0, n1) / max(n0, n1)
                tree.add_feature("stairs2", s / (util.clade_size(tree, tree) - 1))
            return tree.stairs2

    def maximum(self, n, m, mode):
        return float('nan')

    def minimum(self, n, m, mode):
        return float('nan')

    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        return -1


class J1(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.j_one
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("j_one", 0)
                return tree.j_one
            f1 = 1 / sum([util.clade_size(tree, node) for node in tree.traverse() if not node.is_leaf()])
            f2 = 0
            for node in tree.traverse():
                if node.is_leaf():
                    continue
                c = node.children
                s = util.clade_size(tree, node)
                f2 += sum([-util.clade_size(tree, child) * math.log(util.clade_size(tree, child) / s, len(c)) for child in c])
            tree.add_feature("j_one", f1 * f2)
            return tree.j_one

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        return 0


class RogersJIndex(TreeIndex):
    #def evaluate_only(self, tree, mode):
    #    s = 0
    #    for node in tree.traverse("postorder"):
    #        if not node.is_leaf():
    #            if util.balance_index(tree, node) != 0:
    #                s += 1
    #    return s 

    def evaluate(self, tree, mode):
        if mode == "ARBITRARY":
            raise ValueError("rogers_j_index is not defined for arbitrary trees")
        try:
            return tree.rogers_j_index
        except AttributeError:
            s = 0
            for node in tree.traverse("postorder"):
                if not node.is_leaf():
                    if util.balance_index(tree, node) != 0:
                        s += 1
            tree.add_feature("rogers_j_index", s)
            return tree.rogers_j_index

    def maximum(self, n, m, mode):
        if mode == "BINARY":
            if n == 1:
                return 0
            return n - 2
        if mode == "ARBITRARY":
            return float("nan")

    def minimum(self, n, m, mode):
        if mode == "BINARY":
            return bin(n).count("1") - 1
        if mode == "ARBITRARY":
            return float("nan")
    
    def exp_yule(self, n):
        return float("nan")
    
    def imbalance(self):
        return 1


class SymmetryNodesIndex(TreeIndex):
    def evaluate(self, tree, mode):
        if mode == "ARBITRARY":
            raise ValueError("symmetry_nodes_index is not defined for arbitrary trees")
        try:
            return tree.symmetry_nodes_index
        except AttributeError:
            cnt = 0
            for node in tree.traverse("postorder"):
                if not node.is_leaf():
                    c = node.children
                    assert (len(c) == 2)
                    if not util.isomorphic(c[0], c[1]):
                        cnt += 1
            tree.add_feature("symmetry_nodes_index", cnt)
            return tree.symmetry_nodes_index

    def maximum(self, n, m, mode):
        if mode == "BINARY":
            if n == 1:
                return 0
            return n - 2
        if mode == "ARBITRARY":
            return float("nan")

    def minimum(self, n, m, mode):
        if mode == "BINARY":
            return bin(n).count("1") - 1
        if mode == "ARBITRARY":
            return float("nan")

    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        return 1


