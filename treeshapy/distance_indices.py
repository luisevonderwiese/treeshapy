import numpy as np
import math

import treeshapy.util as util
from treeshapy.tree_index import TreeIndex
from treeshapy.depth_indices import SackinIndex

class TotalCopheneticIndex(TreeIndex):
    #def evaluate_only(self, tree, binary):
    #    s = 0
    #    for node in tree.iter_descendants("postorder"):
    #        if not node.is_leaf():
    #            s += math.comb(util.clade_size(tree, node), 2)
    #    return s

    def evaluate(self, tree, binary):
        try:
            return tree.total_cophenetic_index
        except AttributeError:
            s = 0
            for node in tree.iter_descendants("postorder"):
                if not node.is_leaf():
                    s += math.comb(util.clade_size(tree, node), 2)
            tree.add_feature("total_cophenetic_index", s)
            return tree.total_cophenetic_index

    def maximum(self, n, m, binary):
        return math.comb(n, 3)

    def minimum(self, n, m, binary):
        if binary:
            factorial = 1
            s = 0
            for i in range(n):
                a = 1
                j = 0
                if i != 0:
                    factorial *= i
                while (a * 2) <= factorial and factorial % (a * 2) == 0:
                    a *= 2
                    j += 1
                s += j
            return s
        else:
            return 0
    
    def exp_yule(self, n):
        return n * (n + 1) - 2 * n * util.H(n) 
    
class Diameter(TreeIndex):
    def evaluate(self, tree, binary):
        try:
            return tree.diameter
        except AttributeError:
            if tree.is_leaf(): #single-node-tree
                tree.add_feature("diameter", 0)
            else:
                tree.add_feature("diameter", util.diameter(tree))
            return tree.diameter

    def maximum(self, n, m, binary):
        return n

    def minimum(self, n, m, binary):
        if binary:
            return float("nan")
        else:
            if n == 1:
                return 0
            return 2
    
    def exp_yule(self, n):
        return float("nan")
    

class AreaPerPairIndex(TreeIndex):
    def evaluate(self, tree, binary):
        try:
            return tree.area_per_pair_index
        except AttributeError:
            n = util.clade_size(tree, tree)
            if n == 1:
                tree.add_feature("area_per_pair_index", 0)
            else:
                s = SackinIndex().evaluate(tree, binary)
                c = TotalCopheneticIndex().evaluate(tree, binary)
                tree.add_feature("area_per_pair_index", (2 / n) * s - (4 / (n * (n - 1))) * c)
            return tree.area_per_pair_index

    def maximum(self, n, m, binary):
        return float('nan')

    def minimum(self, n, m, binary):
        return float('nan')

    def exp_yule(self, n):
        if n == 1:
            return 0
        a = (n + 1) / (n - 1)
        return 4 * ((util.H(n) - 1) * a - 1)
    


