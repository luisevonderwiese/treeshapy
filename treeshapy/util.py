import math
import numpy as np
import json
import pkg_resources
from collections import Counter

we_dict = None

def leaf_depths(tree):
    return [depth(tree, leaf) for leaf in tree.iter_leaves()]

def clade_size(tree, v):
    try:
        return v.clade_size
    except AttributeError:
        precompute_clade_sizes(tree)
        return v.clade_size

def depth(tree, v):
    try:
        return v.depth
    except AttributeError:
        precompute_depths(tree)
        return v.depth

def precompute_clade_sizes(tree):
    for node in tree.traverse("postorder"):
        if node.is_leaf():
            node.add_feature("clade_size", 1)
            continue
        c = node.children
        node.add_feature("clade_size", sum([child.clade_size for child in c]))


def precompute_depths(tree):
    tree.add_feature("depth", 0)
    depths_recursive(tree)

def depths_recursive(tree):
    c = tree.children
    d = tree.depth + 1
    for child in c:
        child.add_feature("depth", d)
        if not child.is_leaf():
            depths_recursive(child)

def widths(tree):
    return Counter([depth(tree, v) for v in tree.traverse("postorder")])

def connecting_path_length(tree, v1, v2):
    ancestor = tree.get_common_ancestor(v1, v2)
    return depth(tree, v1) + depth(tree, v2) - 2 * depth(tree, ancestor)

def inner_nodes(tree):
    inner_nodes = []
    for v in tree.traverse("postorder"):
        if not v.is_leaf():
            inner_nodes.append(v)
    return inner_nodes

def find_distant_node(tree):
    max_depth = 0
    distant_node = None
    for node in tree.iter_descendants():
        if node.name == "dummy":
            continue
        if node.depth > max_depth:
            max_depth = node.depth
            distant_node = node.name
    return max_depth, distant_node

def diameter(tree):
    _, distant_node = find_distant_node(tree)
    tree_copy = tree.copy("newick")
    tree_copy.add_child(name="dummy") # required to keep the root node
    tree_copy.set_outgroup(tree_copy&distant_node)
    precompute_depths(tree_copy)
    dist, distant_node2 = find_distant_node(tree_copy)
    return dist

def precompute_nodes_below(tree):
    for node in tree.traverse("postorder"):
        node.add_feature("nodes_below", 1)
        if node.is_leaf():
            continue
        for c in node.children:
            node.nodes_below += c.nodes_below

def precompute_farness(tree):
    try:
        tree.nodes_below
    except AttributeError:
        precompute_nodes_below(tree)
    num_nodes = tree.nodes_below
    tree.add_feature("farness", sum([depth(tree, node) for node in tree.traverse()]))
    for node in tree.traverse("preorder"):
        if node.is_leaf():
            continue
        for c in node.children:
            c.add_feature("farness", node.farness - c.nodes_below + (num_nodes - c.nodes_below))

def precompute_bcent(tree):
    try:
        tree.nodes_below
    except AttributeError:
        precompute_nodes_below(tree)
    num_nodes = tree.nodes_below
    for node in tree.traverse():
        if node.is_leaf():
            continue
        node.add_feature("bcent", (node.nodes_below - 1) * (num_nodes - node.nodes_below))
        cs = node.children
        for i, c1 in enumerate(cs):
            for j in range(i + 1, len(cs)):
                c2 = cs[j]
                node.bcent += c1.nodes_below * c2.nodes_below


def precompute_ladder_lengths(tree):
    for node in tree.traverse("postorder"):
        if node.is_leaf():
            node.add_feature("ladder_length", -1)
            continue
        c = node.children
        assert len(c)==2 #only defined for bifurcating trees
        if c[0].is_leaf() and not c[1].is_leaf():
            node.add_feature("ladder_length", c[1].ladder_length + 1)
        elif c[1].is_leaf() and not c[0].is_leaf():
            node.add_feature("ladder_length", c[0].ladder_length + 1)
        else: #not part of a ladder
            node.add_feature("ladder_length", 0)
    for node in tree.traverse("preorder"):
        if node.ladder_length == 1:
            node.ladder_length = 0 #ladders of length 1 do not count
        if node.ladder_length > 0:
            c = node.children
            if c[0].is_leaf():
                assert not c[1].is_leaf()
                if c[1].ladder_length > 0:
                    c[1].ladder_length = node.ladder_length
                    node.ladder_length = 0
            else:
                assert c[1].is_leaf()
                if c[0].ladder_length > 0:
                    c[0].ladder_length = node.ladder_length
                    node.ladder_length = 0

def is_pitchfork(tree, node):
    return clade_size(tree, node) == 3 and len(node.children) == 2

def is_4caterpillar(tree, node):
    if clade_size(tree, node) != 4:
        return False
    c = node.children
    if len(c) != 2:
        return False
    return (c[0].is_leaf() and is_pitchfork(tree, c[1])) or (c[1].is_leaf() and is_pitchfork(tree, c[0]))

def is_double_cherry(tree, node):
    if clade_size(tree, node) != 4:
        return False
    c = node.children
    if len(c) != 2:
        return False
    return (not c[0].is_leaf()) and (not c[1].is_leaf())


def balance_index(tree, v):
    if v.is_leaf():
        return 0
    c = v.children
    assert (len(c) == 2)
    return abs(clade_size(tree, c[0]) - clade_size(tree, c[1]))

def precompute_probs(tree):
    tree.add_feature("prob", 1)
    probs_recursive(tree)

def probs_recursive(tree):
    if tree.is_leaf():
        return
    c = tree.children
    p = tree.prob / len(c)
    for child in c:
        child.add_feature("prob", p)
        if not child.is_leaf():
            probs_recursive(child)

def precompute_heights(tree):
    for node in tree.iter_descendants("postorder"):
        if node.is_leaf():
            node.add_feature("height", 0)
            continue
        c = node.children
        h = 1 + max([child.height for child in c])
        node.add_feature("height", h)

def read_we():
    global we_dict
    if we_dict is not None:
        return
    stream = pkg_resources.resource_stream(__name__, 'resources/we.json')
    we_dict = json.loads(stream.read())
    we_dict = {int(k): int(v) for k, v in we_dict.items()}

def we(n):
    read_we()
    if not n in we_dict:
        return float("nan")
    return we_dict[n]

def furnas_ranks(tree):
    read_we()
    for node in tree.traverse("postorder"):
        if node.is_leaf():
            node.add_feature("furnas_rank", 1)
            continue
        c = node.children
        assert (len(c) == 2)
        if clade_size(tree, c[0]) < clade_size(tree, c[1]) or (clade_size(tree, c[0]) == clade_size(tree, c[1]) and c[0].furnas_rank < c[1].furnas_rank):
            f_l = c[0].furnas_rank
            alpha = clade_size(tree, c[0])
            f_r = c[1].furnas_rank
            beta = clade_size(tree, c[1])
        else:
            f_l = c[1].furnas_rank
            alpha = clade_size(tree, c[1])
            f_r = c[0].furnas_rank
            beta = clade_size(tree, c[0])
        s = 0
        for i in range(1, alpha):
            j = clade_size(tree, node) - i
            if i in we_dict and j in we_dict:
                s += we_dict[i] * we_dict[j]
            else:
                node.add_feature("furnas_rank", float("nan"))
                continue
        if beta in we_dict:
            s += (f_l - 1) * we_dict[beta] + f_r
        else:
            node.add_feature("furnas_rank", float("nan"))
            continue
        if alpha == beta:
            s -= (f_l * f_l - f_l) // 2
        node.add_feature("furnas_rank", int(s))


def isomorphic(v1, v2):
    if v1.is_leaf():
        return v2.is_leaf()
    if v2.is_leaf():
        return False
    c1 = v1.children
    assert (len(c1) == 2)
    c2 = v2.children
    assert (len(c2) == 2)
    return (isomorphic(c1[0], c2[0]) and isomorphic(c1[1], c2[1])) or (isomorphic(c1[0], c2[1]) and isomorphic(c1[1], c2[0]))



def I_value(tree, v):
    c = v.children
    assert (len(c) == 2)
    n_v1 = max(clade_size(tree, c[0]), clade_size(tree, c[1]))
    n_v = clade_size(tree, v)
    half = math.ceil(n_v / 2.0)
    if (n_v - 1 - half) == 0:
        return 0
    return (n_v1 - half) / (n_v - 1 - half)

def I_prime(tree, v):
    I_v = I_value(tree, v)
    n_v = clade_size(tree, v)
    if n_v > 0 and n_v % 2 == 0:
        I_v *= (n_v - 1) / n_v
    return I_v


def I_weight(tree, v):
    n_v = clade_size(tree, v)
    if n_v % 2 == 1:
        return 1
    if n_v == 0:
        return 0
    I_v = I_value(tree, v)
    if I_v == 0:
        return (2 * (n_v - 1)) / n_v
    return (n_v - 1) / n_v

def I_weight_sum(tree):
    weights = []
    for node in tree.traverse("postorder"):
        if clade_size(tree, node) >= 4:
            weights.append(I_weight(tree, node))
    return sum(weights) / len(weights)

def I_w(tree, v, sw):
    return (I_weight(tree, v) * I_value(tree, v)) / sw


def I_values(tree, mode, sw = 0):
    assert(mode in ["I", "I_prime", "I_w"])
    values = []
    for node in tree.traverse("postorder"):
        if clade_size(tree, node) >= 4:
            if mode == "I":
                values.append(I_value(tree, node))
            elif mode == "I_prime":
                values.append(I_prime(tree, node))
            elif mode == "I_w":
                values.append(I_w(tree, node, sw))
    return values

def E_l(n, Xset):
    if n > len(Xset):
        return 0
    if n == len(Xset):
        return math.prod(Xset)
    if n == 1:
        return sum(Xset)
    P = [sum([math.pow(val, x) for val in Xset]) for x in range(1, n+1)]
    mat = [[0 for _ in range(n)] for __ in range(n)]
    for x in range(n):
        mat[x][:x + 1] = P[:x+1][::-1]
    for x in range(n - 1):
        mat[x][x+1] = x + 1
    return np.linalg.det(mat) / math.factorial(n)

def precompute_rqi(tree):
    q = range(5)
    q = [q[0]] + [q[i] - q[0] for i in range(1, 5)]
    for node in tree.traverse("postorder"):
        if node.is_leaf():
            node.add_feature("ypsilon", 0)
            node.add_feature("rooted_quartet_index", 0)
            continue
        n_v = clade_size(tree, node)
        c = node.children
        ccs = [clade_size(tree, child) for child in c]
        E3 = E_l(3, ccs)
        E4 = E_l(4, ccs)
        node.add_feature("ypsilon", sum([child.ypsilon for child in c]) + E3)
        rqi = sum([child.rooted_quartet_index for child in c])
        rqi += q[4] * E4 #star
        rqi += q[3] * E_l(2, [math.comb(cs, 2) for cs in ccs]) #fully balanced
        rqi += q[2] * (clade_size(tree, node) * (node.ypsilon - E3) - \
                sum([clade_size(tree, child) * child.ypsilon for child in c])) #3-pitchfork  + 1
        rqi += q[1] * (0.5 * E3 * E_l(1, ccs) - 2 * E4 - 1.5 * E3) # cherry + 2
        node.add_feature("rooted_quartet_index", rqi)
    tree.rooted_quartet_index = tree.rooted_quartet_index + q[0] * math.comb(clade_size(tree, tree), 4)


def colijn_plazotta_recursive(node):
    if node.is_leaf():
        node.add_feature("colijn_plazotta_rank", 1)
        return
    c = node.children
    assert len(c) == 2
    colijn_plazotta_recursive(c[0])
    colijn_plazotta_recursive(c[1])
    r_0 = c[0].colijn_plazotta_rank
    r_1 = c[1].colijn_plazotta_rank
    if r_0 >= r_1:
        node.add_feature("colijn_plazotta_rank", (r_0 * (r_0 - 1)) / 2 + r_1 + 1)
    else:
        node.add_feature("colijn_plazotta_rank", (r_1 * (r_1 - 1)) / 2 + r_0 + 1)


def wiener_index_recursive(node):
    if node.is_leaf():
        node.add_feature("S_1", 0)
        node.add_feature("wiener_index", 0)
        return
    c = node.children
    n = node.nodes_below
    S_1 = 0
    S_2 = 0
    S_3 = 0
    for child in c:
        wiener_index_recursive(child)
        n_i = child.nodes_below
        S_1 += child.S_1 + n_i
        S_2 += child.wiener_index
        S_3 += child.S_1 * (n - 1 - n_i) - (n_i * n_i)
    S_3 += (n - 1) * (n - 1)
    node.add_feature("S_1", S_1)
    node.add_feature("wiener_index", S_1 + S_2 + S_3)



def is_bifurcating(tree):
    try: #check if heights already precomputed
        return tree.bifurcating
    except AttributeError:
        tree.add_feature("bifurcating", bifurcating_recursive(tree))
        return tree.bifurcating

def bifurcating_recursive(tree):
    c = tree.children
    if len(c) == 2:
        return bifurcating_recursive(c[0]) and bifurcating_recursive(c[1])
    if len(c) == 0:
        return True
    return False
