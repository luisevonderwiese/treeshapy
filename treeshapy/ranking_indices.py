import treeshapy.util as util
from treeshapy.tree_index import TreeIndex

class ColijnPlazottaRank(TreeIndex):
    def evaluate(self, tree, mode):
        if mode == "ARBITRARY":
            raise ValueError("colijn_plazotta_rank is not defined for arbitrary trees")
        try:
            return tree.colijn_plazotta_rank
        except AttributeError:
            util.colijn_plazotta_recursive(tree)
            return tree.colijn_plazotta_rank

    def maximum(self, n, m, mode):
        return float('nan')

    def minimum(self, n, m, mode):
        return float('nan')

    def exp_yule(self, n):
        return float("nan")


class FurnasRank(TreeIndex):
    def evaluate(self, tree, mode):
        if mode == "ARBITRARY":
            raise ValueError("furnas_rank is not defined for arbitrary trees")
        try:
            return tree.furnas_rank #check if furnas ranks already precomputed
        except AttributeError:
            util.furnas_ranks(tree)
            return tree.furnas_rank

    def maximum(self, n, m, mode):
        if mode == "BINARY":
            return util.we(n)
        if mode == "ABITRARY":
            return float("nan")

    def minimum(self, n, m, mode):
        if mode == "BINARY":
            return 1
        if mode == "ARBITRARY":
            return float("nan")

    def exp_yule(self, n):
        return float("nan")
