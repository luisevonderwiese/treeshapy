import math

import treeshapy.util as util
from treeshapy.tree_index import TreeIndex

class CherryIndex(TreeIndex):
    def evaluate_only(self, tree, mode):
        cnt = 0
        for node in tree.traverse("postorder"):
            if node.is_leaf():
                continue
            direct_leaves = len([child for child in node.children if child.is_leaf()])
            if direct_leaves >= 2:
                cnt += math.comb(direct_leaves, 2)
        return  cnt

    def evaluate(self, tree, mode):
        try:
            return tree.cherry_index
        except AttributeError:
            cnt = 0
            for node in tree.traverse("postorder"):
                if node.is_leaf():
                    continue
                direct_leaves = len([child for child in node.children if child.is_leaf()])
                if direct_leaves >= 2:
                    cnt += math.comb(direct_leaves, 2)
            tree.add_feature("cherry_index", cnt)
            return tree.cherry_index

    def maximum(self, n, m, mode):
        if mode == "BINARY":
            return math.floor(n / 2)
        if mode == "ARBITRARY":
            return math.comb(n, 2)

    def minimum(self, n, m, mode):
        if n == 1:
            return 0
        return 1

    def exp_yule(self, n):
        if n < 3:
            return n - 1
        return n / 3

    def imbalance(self):
        return 0


class ModifiedCherryIndex(TreeIndex):
    def evaluate(self, tree, mode):
        if mode == "ARBITRARY":
            raise ValueError("modified_cherry_index is not defined for arbitrary trees")
        try:
            return tree.modified_cherry_index
        except AttributeError:
            tree.add_feature("modified_cherry_index", util.clade_size(tree, tree) - 2 * CherryIndex().evaluate_only(tree, mode))
            return tree.modified_cherry_index

    def maximum(self, n, m, mode):
        if mode == "BINARY":
            if n == 1:
                return 1
            return n - 2
        if mode == "ARBITRARY":
            return float("nan")

    def minimum(self, n, m, mode):
        if mode == "BINARY":
            return n % 2
        if mode == "ARBITRARY":
            return float("nan")
    
    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        return 0

class Pitchforks(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.pitchforks
        except AttributeError:
            cnt = 0
            for node in tree.traverse():
                if util.is_pitchfork(tree, node):
                    cnt += 1
            tree.add_feature("pitchforks", cnt)
            return tree.pitchforks

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        return 0

class FourCaterpillars(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.four_caterpillars
        except AttributeError:
            cnt = 0
            for node in tree.traverse():
                if util.is_4caterpillar(tree, node):
                    cnt += 1
            tree.add_feature("four_caterpillars", cnt)
            return tree.four_caterpillars

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        return 0

class DoubleCherries(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.double_cherries
        except AttributeError:
            cnt = 0
            for node in tree.traverse():
                if util.is_double_cherry(tree, node):
                    cnt += 1
            tree.add_feature("double_cherries", cnt)
            return tree.double_cherries

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

    def imbalance(self):
        return 0

