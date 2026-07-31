import math
import sys
from copy import deepcopy

import treeshapy.depth_indices as depth_indices
import treeshapy.width_indices as width_indices
import treeshapy.structure_indices as structure_indices
import treeshapy.subgraph_indices as subgraph_indices
import treeshapy.distance_indices as distance_indices
import treeshapy.network_indices as network_indices
import treeshapy.root_indices as root_indices
import treeshapy.node_indices as node_indices
import treeshapy.Ibased_indices as Ibased_indices
import treeshapy.ranking_indices as ranking_indices
import treeshapy.util as util
import treeshapy.index_lists as index_lists

sys.set_int_max_str_digits(2147483647) 


INDICES = list(index_lists.INDICES.keys())

class TreeShape:
    def __init__(self, tree, binary = "auto", rooted = "auto"):
        leaf_names = [l.name for l in tree.iter_leaves()]
        if len(leaf_names) != len(set(leaf_names)):
            raise ValueError("Leaf names must be unique")
        self.tree = tree
        if rooted == "auto":
            self.rooted = (len(self.tree.children) == 2)
        else:
            self.rooted = rooted
            if not self.rooted and not len(self.tree.children) in [0, 2]:
                print("Warning: Removing implitict root")
                self.tree = util.remove_implicit_root(self.tree)
        bifurcating = util.is_bifurcating(self.tree, self.rooted)
        if binary == "auto":
            self.binary = bifurcating
        else:
            self.binary = binary
            if self.binary and not bifurcating:
                raise ValueError("Input tree contains polytomies. Set binary = False or binary = \"auto\" or resolve polytomies in the input tree")
            if not self.binary and bifurcating:
                print("Warning: Input Tree is binary but will be considered as multifurcating. Not all indices are available and normalization is changed")
        if self.rooted and len(self.tree.children) > 2:
            if self.binary:
                raise ValueError("Input Tree is unrooted. Set rooted = False or rooted =  \"auto\" or root the input tree")
            else:
                print("Warning: Tree is considered as rooted, multifurcation at root")
            
        self.n = len(tree)
        if binary:
            if rooted:
                self.m = self.n - 1
            else:
                self.m = self.n - 2
        else:
            self.m = len([node for node in self.tree.traverse()]) - self.n
        self._indices = {}

        if not self.rooted:
            self._all_rooted_trees = None
            self._ts_instances = None

    def _index(self, index_name):
        if index_name not in self._indices:
            instance = self._index_instance(index_name)
            if instance is None:
                raise ValueError(f"Unknown index: {index_name}")
            self._indices[index_name] = instance
        return self._indices[index_name]

    def _absolute(self, index_name):
        return self._index(index_name).evaluate(self.tree, self.binary)

    
    def _relative(self, index_name, rel):
        v = self._absolute(index_name)
        if rel == "MAX":
            min_v = self._index(index_name).minimum(self.n, self.m, self.binary)
            max_v = self._index(index_name).maximum(self.n, self.m, self.binary)
            if (not isinstance(min_v, int) and math.isnan(min_v)) or (not isinstance(max_v, int) and math.isnan(max_v)):
                return float("nan")
            if min_v == max_v:
                raise ValueError(f"Minimum equals maximum for {index_name} for {self.mode.lower()} trees")
            if max_v - v < -0.00001:
                raise ArithmeticError(f"Value above maximum for {index_name}")
            if v - min_v < -0.00001:
                raise ArithmeticError(f"Value below minimum for {index_name}")
            return (v - min_v) / (max_v - min_v)
        if rel == "YULE":
            e = self._index(index_name).exp_yule(self.n)
            if math.isnan(e):
                return float("nan")
            return (v - e) / self.n
        if rel == "TIPS":
            return v / self.n
        raise ValueError(f"REL_{rel} is not a evaluation mode. Choose from ABS, REL_TIPS, REL_MAX, REL_YULE")
    
    def evaluate(self, param, eval_mode = "ABS"):
        if isinstance(param, str) and param != "all":
            if eval_mode == "ABS":
                return self._absolute(param)
            elif eval_mode.startswith("REL"):
                return self._relative(param, eval_mode.split("_")[1])
            else:
                raise ValueError(f"{eval_mode} is not an evaluation mode. Choose from ABS, REL_TIPS, REL_MAX, REL_YULE")
        elif param == "all":
            return {index : self.evaluate(index, eval_mode) for index in self.index_list(eval_mode)}
        else:
            return {index : self.evaluate(index, eval_mode) for index in self.index_list(param)}
        
    def index_list(self, param = "ABS"):
        if isinstance(param, str): # param is eval_mode
            return index_lists.get_list(self.binary, self.rooted, param)
        if not isinstance(param, int):
            raise ValueError(f"Illegal Argument: {param}")
        if not self.binary and self.rooted:
            raise ValueError("Subsets only defined for binary rooted trees")
        return index_lists.get_subset(param)

    def evaluate_for_all_roots(self, param, eval_mode = "ABS"):
        if self.rooted: 
            raise ValueError("All roots mode only possible for unrooted trees")
        if self._all_rooted_trees is None:
            self._all_rooted_trees = self._find_all_rooted_trees(self.tree)
        if self._ts_instances is None:
            self._ts_instances = {name : TreeShape(tree, self.binary, True) for name, tree in self._all_rooted_trees.items()}
        return {branch_name : ts.evaluate(param, eval_mode) for branch_name, ts in self._ts_instances.items()}
    
    def index_list_for_all_roots(self, param):
        if self.rooted:
            raise ValueError("All roots mode only possible for unrooted trees")
        if isinstance(param, str): # param is eval_mode
            return index_lists.get_list(self.binary, True, param)
        if not isinstance(param, int):
            raise ValueError(f"Illegal Argument: {param}")
        if not self.binary:
            raise ValueError("Subsets only defined for binary rooted trees")
        return index_lists.get_subset(param)

    def get_all_rooted_trees(self):
        if self._all_rooted_trees is None:
            self._all_rooted_trees = self._find_all_rooted_trees(self.tree)
        return self._all_rooted_trees



    def _find_all_rooted_trees(self, tree):
        internal_count = 0
        node_names = []
        for node in tree.iter_descendants():
            if not node.is_leaf():
                node.name = "internal_" + str(internal_count)
                internal_count += 1
            node_names.append(node.name)
        rooted_trees = {}
        for name in node_names:
            rooted_tree = deepcopy(tree)
            root = rooted_tree&name
            rooted_tree.set_outgroup(root)
            rooted_trees[name] = rooted_tree
        return rooted_trees


    def _index_instance(self, index_name):
        match index_name:
            case "colless_index":
                return node_indices.CollessIndex()
            case "corrected_colless_index":
                return node_indices.CorrectedCollessIndex()
            case "quadratic_colless_index":
                return node_indices.QuadraticCollessIndex()
            case "I_2_index":
                return node_indices.I2Index()
            case "stairs1":
                return node_indices.Stairs1()
            case "stairs2":
                return node_indices.Stairs2()
            case "j1":
                return node_indices.J1()
            case "rogers_j_index":
                return node_indices.RogersJIndex()
            case "symmetry_nodes_index":
                return node_indices.SymmetryNodesIndex()
            case "mean_I":
                return Ibased_indices.MeanI()
            case "mean_I_prime":
                return Ibased_indices.MeanIPrime()
            case "mean_I_w":
                return Ibased_indices.MeanIW()
            case "total_I":
                return Ibased_indices.TotalI()
            case "total_I_prime":
                return Ibased_indices.TotalIPrime()
            case "total_I_w":
                return Ibased_indices.TotalIW()
            case "sackin_index":
                return depth_indices.SackinIndex()
            case "total_path_length":
                return depth_indices.TotalPathLength()
            case "total_internal_path_length":
                return depth_indices.TotalInternalPathLength()
            case "average_vertex_depth":
                return depth_indices.AverageVertexDepth()
            case "average_leaf_depth":
                return depth_indices.AverageLeafDepth()
            case "variance_of_leaves_depths":
                return depth_indices.VarianceOfLeavesDepths()
            case "average_vertex_depth":
                return depth_indices.AverageVertexDepth()
            case "maximum_depth":
                return depth_indices.MaximumDepth()
            case "s_shape":
                return depth_indices.SShape()
            case "B_1_index":
                return depth_indices.B1Index()
            case "B_2_index":
                return depth_indices.B2Index()
            case "maximum_width":
                return width_indices.MaximumWidth()
            case "maxdiff_widths":
                return width_indices.MaxdiffWidths()
            case "modified_maxdiff_widths":
                return width_indices.ModifiedMaxdiffWidths()
            case "max_width_over_max_depth":
                return width_indices.MaxWidthOverMaxDepth()
            case "d_index":
                return structure_indices.DIndex()
            case "rooted_quartet_index":
                return structure_indices.RootedQuartetIndex()
            case "average_ladder":
                return structure_indices.AverageLadder()
            case "ladder_length":
                return structure_indices.LadderLength()
            case "cherry_index":
                return subgraph_indices.CherryIndex()
            case "modified_cherry_index":
                return subgraph_indices.ModifiedCherryIndex()
            case "IL_number":
                return subgraph_indices.ILNumber()
            case "pitchforks":
                return subgraph_indices.Pitchforks()
            case "four_caterpillars":
                return subgraph_indices.FourCaterpillars()
            case "double_cherries":
                return subgraph_indices.DoubleCherries()
            case "total_cophenetic_index":
                return distance_indices.TotalCopheneticIndex()
            case "diameter":
                return distance_indices.Diameter()
            case "area_per_pair_index":
                return distance_indices.AreaPerPairIndex()
            case "wiener_index":
                return network_indices.WienerIndex()
            case "maximum_closeness":
                return network_indices.MaximumCloseness()
            case "minimum_farness":
                return network_indices.MinimumFarness()
            case "maximum_farness":
                return network_indices.MaximumFarness()
            case "total_farness":
                return network_indices.TotalFarness()
            case "minimum_bcent":
                return network_indices.MinimumBCent()
            case "maximum_bcent":
                return network_indices.MaximumBCent()
            case "mean_bcent":
                return network_indices.MeanBCent()
            case "bcent_variance":
                return network_indices.BCentVariance()
            case "bcent_root":
                return network_indices.BCentRoot()
            case "root_imbalance":
                return root_indices.RootImbalance()
            case "I_root":
                return root_indices.IRoot()
            case "colijn_plazotta_rank":
                return ranking_indices.ColijnPlazottaRank()
            case "furnas_rank":
                return ranking_indices.FurnasRank()
        return None
