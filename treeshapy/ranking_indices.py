import treeshapy.util as util
from treeshapy.tree_index import TreeIndex

class ColijnPlazottaRank(TreeIndex):
    def evaluate(self, tree, binary):
        if not binary:
            raise ValueError("colijn_plazotta_rank is not defined for arbitrary trees")
        try:
            return tree.colijn_plazotta_rank
        except AttributeError:
            util.colijn_plazotta_recursive(tree)
            return tree.colijn_plazotta_rank

    def maximum(self, n, m, binary):
        return float('nan')

    def minimum(self, n, m, binary):
        return float('nan')

    def exp_yule(self, n):
        return float("nan")


class FurnasRank(TreeIndex):
    def evaluate(self, tree, binary):
        if not binary:
            raise ValueError("furnas_rank is not defined for arbitrary trees")
        try:
            return tree.furnas_rank #check if furnas ranks already precomputed
        except AttributeError:
            util.furnas_ranks(tree)
            return tree.furnas_rank

    def maximum(self, n, m, binary):
        #if binary:
        #    return util.we(n)
        return float("nan")

    def minimum(self, n, m, binary):
        if binary:
            return 1
        else:
            return float("nan")

    def exp_yule(self, n):
        return float("nan")
