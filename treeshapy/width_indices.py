import treeshapy.util as util
from treeshapy.tree_index import TreeIndex
from treeshapy.depth_indices import MaximumDepth

class MaximumWidth(TreeIndex):
    #def evaluate_only(self, tree, binary):
    #    return max(util.widths(tree).values())

    def evaluate(self, tree, binary):
        try:
            return tree.maximum_width
        except AttributeError:
            tree.add_feature("maximum_width", max(util.widths(tree).values()))
            return tree.maximum_width

    def maximum(self, n, m, binary):
        if binary:
            return float("nan")
        else:
            return n

    def minimum(self, n, m, binary):
        if n == 1:
            return 1
        return 2

    def exp_yule(self, n):
        return float("nan")



class MaxdiffWidths(TreeIndex):
    def evaluate(self, tree, binary):
        try:
            return tree.maxdiff_widths
        except AttributeError:
            w = util.widths(tree)
            res = 0
            for i in range(len(w) - 1):
                diff = abs(w[i + 1] - w[i])
                res = max(res, diff)
            tree.add_feature("maxdiff_widths", res)
            return tree.maxdiff_widths

    def maximum(self, n, m, binary):
        if binary:
            return float("nan")
        else:
            return n - 1

    def minimum(self, n, m, binary):
        if n == 1:
            return 0
        return 1

    def exp_yule(self, n):
        return float("nan")


class ModifiedMaxdiffWidths(TreeIndex):
    def evaluate(self, tree, binary):
        try:
            return tree.modified_maxdiff_widths
        except AttributeError:
            w = util.widths(tree)
            res = 0
            for i in range(len(w) - 1):
                diff = w[i + 1] - w[i]
                res = max(res, diff)
            tree.add_feature("modified_maxdiff_widths", res)
            return tree.modified_maxdiff_widths

    def maximum(self, n, m, binary):
        if binary:
            return float("nan")
        else:
            return n - 1

    def minimum(self, n, m, binary):
        if n == 1:
            return 0
        return 1

    def exp_yule(self, n):
        return float("nan")


class MaxWidthOverMaxDepth(TreeIndex):
    def evaluate(self, tree, binary):
        try:
            return tree.max_width_over_max_depth
        except AttributeError:
            h = MaximumDepth().evaluate(tree, binary)
            if h == 0:
                tree.add_feature("max_width_over_max_depth", 0)
            else:
                tree.add_feature("max_width_over_max_depth", MaximumWidth().evaluate(tree, binary) / h)
            return tree.max_width_over_max_depth

    def maximum(self, n, m, binary):
        return float('nan')

    def minimum(self, n, m, binary):
        if n == 1:
            return 0
        return 2 / (n - 1)

    def exp_yule(self, n):
        return float("nan")

