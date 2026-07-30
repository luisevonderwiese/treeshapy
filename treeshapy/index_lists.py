
#"index_name" : [
#   defined for multifurcating trees
#   can be normalized by maximum value for binary trees
#   can be normalized by maximum for multifurcating trees
#   can by normalized by expected value under the yule model (binary trees only)
#   defined for unrooted trees ]

INDICES = {
        "colless_index" : [False, True, False, True, False],
        "corrected_colless_index" : [False, True, False, True, False],
        "quadratic_colless_index" : [False, True, False, True, False],
        "I_2_index" : [False, True, False, False, False],
        "stairs1" : [False, True, False, False, False],
        "stairs2" : [False, False, False, False, False],
        "j1" : [True, False, False, False, False],
        "rogers_j_index" : [False, True, False, False, False],
        "symmetry_nodes_index" : [False, True, False, False, False],
        
        "mean_I" : [False, False, False, False, False],
        "mean_I_prime" : [False, False, False, False, False],
        "mean_I_w" : [False, False, False, False, False],
        "total_I" : [False, False, False, False, False],
        "total_I_prime" : [False, False, False, False, False],
        "total_I_w" : [False, False, False, False, False],
        
        "sackin_index" : [True, True, True, True, False],
        "total_path_length" : [True, True, True, False, False],
        "total_internal_path_length" : [True, True, True, False, False],
        "average_vertex_depth" : [True, True, True, False, False],
        "average_leaf_depth" : [True, True, True, True, False],
        "variance_of_leaves_depths" : [True, False, True, True, False],
        "maximum_depth" : [True, True, True, False, False],
        "s_shape" : [True, False, True, False, False],
        "B_1_index" : [True, False, False, False, False],
        "B_2_index" : [True, True, True, True, False],

        "maximum_width" : [True, False, True, False, False],
        "maxdiff_widths" : [True, False, True, False, False],
        "modified_maxdiff_widths" : [True, False, True, False, False],
        "max_width_over_max_depth" : [True, False, False, False, False],
        
        "d_index" : [True, False, False, False, False],
        "rooted_quartet_index" : [True, False, True, True, False],
        "average_ladder" : [False, False, False, False, False],
        "ladder_length" : [False, False, False, False, False],
        
        "cherry_index" : [True, True, True, True, False],
        "modified_cherry_index" : [False, True, False, False, False],
        "IL_number" : [True, False, False, False, False],
        "pitchforks" : [True, False, False, False, False],
        "four_caterpillars" : [True, False, False, False, False],
        "double_cherries" : [True, False, False, False, False],
        
        "total_cophenetic_index" : [True, True, True, True, False],
        "diameter" : [True, False, True, False, True],
        "area_per_pair_index" : [True, False, False, True, True],
        
        "wiener_index" : [True, False, False, False, True],
        "maximum_closeness" : [True, False, False, False, True],
        "minimum_farness" : [True, False, False, False, True],
        "maximum_farness" : [True, False, False, False, True],
        "total_farness" : [True, False, False, False, True],
        "minimum_bcent" : [True, False, False, False, True],
        "maximum_bcent": [True, False, False, False, True],
        "mean_bcent" : [True, False, False, False, True],
        "bcent_variance" : [True, False, False, False, True],
        "bcent_root" : [True, False, False, False, False],
        
        "root_imbalance" : [False, True, False, False, False],
        "I_root" : [False, True, False, False, False],
        
        "colijn_plazotta_rank" : [False, False, False, False, False],
        "furnas_rank" : [False, True, False, False, False]
}


INDEX_SUBSETS = {   2 : ['maximum_width', 'stairs1'],
                    3 : ['bcent_root', 'root_imbalance', 'I_2_index'],
                    4 : ['corrected_colless_index', 'average_ladder', 'I_root', 'stairs1'],
                    5 : ['corrected_colless_index', 'maxdiff_widths', 'average_ladder', 'I_root', 'stairs1'],
                    6 : ['B_2_index', 'maxdiff_widths', 'cherry_index', 'average_ladder', 'I_root', 'stairs1'],
                    7 : ['variance_of_leaves_depths', 'corrected_colless_index', 'B_2_index', 'maxdiff_widths', 'average_ladder', 'I_root', 'stairs1'],
                    8 : ['B_2_index', 'maxdiff_widths', 'modified_maxdiff_widths', 'cherry_index', 'average_ladder', 'I_root', 'stairs1', 'mean_I_prime'],
                    9 : ['variance_of_leaves_depths', 'corrected_colless_index', 'B_2_index', 'maxdiff_widths', 'modified_maxdiff_widths', 'average_ladder', 'I_root', 'stairs1', 'I_2_index'],
                    10 : ['B_1_index', 'B_2_index', 'maxdiff_widths', 'modified_maxdiff_widths', 'cherry_index', 'average_ladder', 'I_root', 'stairs1', 'mean_I_prime', 'mean_I_w']}



def get_list(binary, rooted, eval_mode):
    index_list = list(INDICES.keys())
    if not binary:
        index_list = [index for index in index_list if INDICES[index][0]]
    if not rooted:
        index_list = [index for index in index_list if INDICES[index][4]]
    if eval_mode in ["ABS", "REL_TIPS"]:
        return index_list
    if eval_mode  == "REL_MAX":
        if binary:
            return [index for index in index_list if INDICES[index][1]]
        else:
            return [index for index in index_list if INDICES[index][2]]
    if eval_mode == "REL_YULE":
        if binary:
            return [index for index in index_list if INDICES[index][3]]
        else:
            raise ValueError("REL_YULE not possile for multifurcating trees")
    raise ValueError(f"{eval_mode} is not an evaluation mode! Choose from ABS, REL_TIPS, REL_MAX, REL_YULE")

def get_subset(k):
    if k not in INDEX_SUBSETS:
        raise ValueError(f"No subset of length {k}")
    return INDEX_SUBSETS[k]
