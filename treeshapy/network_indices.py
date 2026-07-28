import numpy as np

import treeshapy.util as util
from treeshapy.tree_index import TreeIndex
from treeshapy.depth_indices import SackinIndex
from treeshapy.distance_indices import AreaPerPairIndex 

class WienerIndex(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.wiener_index
        except AttributeError:
            try:
                tree.nodes_below
            except AttributeError:
                util.precompute_nodes_below(tree)
            util.wiener_index_recursive(tree)
            return tree.wiener_index

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

class MaximumCloseness(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.maximum_closeness
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("maximum_closeness", float("nan"))
                return tree.maximum_closeness
            try:
                tree.farness
            except AttributeError:
                util.precompute_farness(tree)
            tree.add_feature("maximum_closeness", max([1 / node.farness for node in tree.traverse()]))
            return tree.maximum_closeness

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

class MinimumFarness(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.minimum_farness
        except AttributeError:
            try:
                tree.farness
            except AttributeError:
                util.precompute_farness(tree)
            tree.add_feature("minimum_farness", min([node.farness for node in tree.traverse()]))
            return tree.minimum_farness

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")
    
class MaximumFarness(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.maximum_farness
        except AttributeError:
            try:
                tree.farness
            except AttributeError:
                util.precompute_farness(tree)
            tree.add_feature("maximum_farness", max([node.farness for node in tree.traverse()]))
            return tree.maximum_farness

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")
    
    def exp_yule(self, n):
        return float("nan")
    
class TotalFarness(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.total_farness
        except AttributeError:
            try:
                tree.farness
            except AttributeError:
                util.precompute_farness(tree)
            tree.add_feature("total_farness", sum([node.farness for node in tree.traverse()]))
            return tree.total_farness

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")
    
class MinimumBCent(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.minimum_bcent
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("minimum_bcent", 0)
            else:
                try:
                    tree.bcent
                except AttributeError:
                    util.precompute_bcent(tree)
                tree.add_feature("minimum_bcent", min([node.bcent for node in tree.traverse() if not node.is_leaf()]))
            return tree.minimum_bcent

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")
    
class MaximumBCent(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.maximum_bcent
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("maximum_bcent", 0)
            else:
                try:  
                    tree.bcent
                except AttributeError:
                    util.precompute_bcent(tree)
                tree.add_feature("maximum_bcent", max([node.bcent for node in tree.traverse() if not node.is_leaf()]))
            return tree.maximum_bcent

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

class MeanBCent(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.mean_bcent
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("mean_bcent", 0)
            else:
                try:
                    tree.bcent
                except AttributeError:
                    util.precompute_bcent(tree)
                bcents = [node.bcent for node in tree.traverse() if not node.is_leaf()]
                tree.add_feature("mean_bcent", sum(bcents) / len(bcents))
            return tree.mean_bcent

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

class BCentVariance(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            return tree.bcent_variance
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("bcent_variance", 0)
            else:
                try:
                    tree.bcent
                except AttributeError:
                    util.precompute_bcent(tree)
                bcents = [node.bcent for node in tree.traverse() if not node.is_leaf()]
                tree.add_feature("bcent_variance", np.var(bcents))
            return tree.bcent_variance

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")    

class BCentRoot(TreeIndex):
    def evaluate(self, tree, mode):
        try:
            tree.bcent
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("bcent", 0)
            else:
                util.precompute_bcent(tree)
        return tree.bcent

    def maximum(self, n, m, mode):
        return float("nan")

    def minimum(self, n, m, mode):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")


