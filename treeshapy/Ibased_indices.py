import treeshapy.util as util
from treeshapy.tree_index import TreeIndex

class MeanI(TreeIndex):
    def evaluate(self, tree, binary):
        if not binary:
            raise ValueError("mean_I is not defined for arbitrary trees")
        try:
            return tree.mean_I
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("mean_I", 0)
            else:
                values = util.I_values(tree, "I")
                tree.add_feature("mean_I", sum(values) / len(values))
            return tree.mean_I

    def maximum(self, n, m, binary):
        return float("nan")

    def minimum(self, n, m, binary):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

class MeanIPrime(TreeIndex):
    def evaluate(self, tree, binary):
        if not binary:
            raise ValueError("mean_I_prime is not defined for arbitrary trees")
        try:
            return tree.mean_I_prime
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("mean_I_prime", 0)
            else:
                values = util.I_values(tree, "I_prime")
                tree.add_feature("mean_I_prime", sum(values) / len(values))
            return tree.mean_I_prime

    def maximum(self, n, m, binary):
        return float("nan")

    def minimum(self, n, m, binary):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

class MeanIW(TreeIndex):
    def evaluate(self, tree, binary):
        if not binary:
            raise ValueError("mean_I_w is not defined for arbitrary trees")
        try:
            return tree.mean_I_w
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("mean_I_w", 0)
            else:
                sw = util.I_weight_sum(tree)
                values = util.I_values(tree, "I_w", sw)
                tree.add_feature("mean_I_w", sum(values) / len(values))
            return tree.mean_I_w

    def maximum(self, n, m, binary):
        return float("nan")

    def minimum(self, n, m, binary):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")


class TotalI(TreeIndex):
    def evaluate(self, tree, binary):
        if not binary:
            raise ValueError("total_I is not defined for arbitrary trees")
        try:
            return tree.total_I
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("total_I", 0)
            else:
                tree.add_feature("total_I", sum(util.I_values(tree, "I")))
            return tree.total_I

    def maximum(self, n, m, binary):
        return float("nan")

    def minimum(self, n, m, binary):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")
    

class TotalIPrime(TreeIndex):
    def evaluate(self, tree, binary):
        if not binary:
            raise ValueError("total_I_prime is not defined for arbitrary trees")
        try:
            return tree.total_I_prime
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("total_I_prime", 0)
            else:
                tree.add_feature("total_I_prime", sum(util.I_values(tree, "I_prime")))
            return tree.total_I_prime

    def maximum(self, n, m, binary):
        return float("nan")

    def minimum(self, n, m, binary):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")

class TotalIW(TreeIndex):
    def evaluate(self, tree, binary):
        if not binary:
            raise ValueError("total_I_w is not defined for arbitrary trees")
        try:
            return tree.total_I_w
        except AttributeError:
            if tree.is_leaf():
                tree.add_feature("total_I_w", 0)
            else:
                sw = util.I_weight_sum(tree)
                tree.add_feature("total_I_w", sum(util.I_values(tree, "I_w", sw)))
            return tree.total_I_w

    def maximum(self, n, m, binary):
        return float("nan")

    def minimum(self, n, m, binary):
        return float("nan")

    def exp_yule(self, n):
        return float("nan")
