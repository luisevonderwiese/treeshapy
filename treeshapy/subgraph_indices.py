import math

import treeshapy.util as util
from treeshapy.tree_index import TreeIndex

class CherryIndex(TreeIndex):
    #def evaluate_only(self, tree, binary):
    #    cnt = 0
    #    for node in tree.traverse("postorder"):
    #        if node.is_leaf():
    #            continue
    #        direct_leaves = len([child for child in node.children if child.is_leaf()])
    #        if direct_leaves >= 2:
    #            cnt += math.comb(direct_leaves, 2)
    #    return  cnt

    def evaluate(self, tree, binary):
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

    def maximum(self, n, m, binary):
        if binary:
            return math.floor(n / 2)
        else:
            return math.comb(n, 2)

    def minimum(self, n, m, binary):
        if n == 1:
            return 0
        return 1

    def exp_yule(self, n):
        if n < 3:
            return n - 1
        return n / 3


class ModifiedCherryIndex(TreeIndex):
    def evaluate(self, tree, binary):
        if not binary:
            raise ValueError("modified_cherry_index is not defined for arbitrary trees")
        try:
            return tree.modified_cherry_index
        except AttributeError:
            tree.add_feature("modified_cherry_index", util.clade_size(tree, tree) - 2 * CherryIndex().evaluate(tree, binary))
            return tree.modified_cherry_index

    def maximum(self, n, m, binary):
        if binary:
            if n == 1:
                return 1
            return n - 2
        else:
            return float("nan")

    def minimum(self, n, m, binary):
        if binary:
            return n % 2
        else:
            return float("nan")
    
    def exp_yule(self, n):
        return float("nan")


class ILNumber(TreeIndex):
    def evaluate(self, tree, binary):
        try:
            return tree.IL_number
        except AttributeError:
            cnt = 0
            for node in tree.traverse("postorder"):
                if len([c for c in node.children if c.is_leaf()]) == 1:
                    cnt += 1
            tree.add_feature("IL_number", cnt)
            return tree.IL_number

    def maximum(self, n, m, binary):
        return float("nan")

    def minimum(self, n, m, binary):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")



class Pitchforks(TreeIndex):
    def evaluate(self, tree, binary):
        try:
            return tree.pitchforks
        except AttributeError:
            cnt = 0
            for node in tree.traverse():
                if util.is_pitchfork(tree, node):
                    cnt += 1
            tree.add_feature("pitchforks", cnt)
            return tree.pitchforks

    def maximum(self, n, m, binary):
        return float("nan")

    def minimum(self, n, m, binary):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

class FourCaterpillars(TreeIndex):
    def evaluate(self, tree, binary):
        try:
            return tree.four_caterpillars
        except AttributeError:
            cnt = 0
            for node in tree.traverse():
                if util.is_4caterpillar(tree, node):
                    cnt += 1
            tree.add_feature("four_caterpillars", cnt)
            return tree.four_caterpillars

    def maximum(self, n, m, binary):
        return float("nan")

    def minimum(self, n, m, binary):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

class DoubleCherries(TreeIndex):
    def evaluate(self, tree, binary):
        try:
            return tree.double_cherries
        except AttributeError:
            cnt = 0
            for node in tree.traverse():
                if util.is_double_cherry(tree, node):
                    cnt += 1
            tree.add_feature("double_cherries", cnt)
            return tree.double_cherries

    def maximum(self, n, m, binary):
        return float("nan")

    def minimum(self, n, m, binary):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

