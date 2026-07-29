from ete3 import Tree

import treeshapy
from treeshapy import TreeShape
from treeshapy import AllRootTreeShape

#list of all implemented indices
print(treeshapy.INDICES)
#list of implemented indices defined for unrooted trees
print(treeshapy.INDICES_UNROOTED)

#read tree
t = Tree("example_rooted.tree")
#initialize treeshape object, set mode = "ARBITRARY" for a tree which is not binary
ts = TreeShape(t, mode = "BINARY", rooted = True)

#evaluate colless index (absolute)
c = ts.absolute("colless_index")
print(c)
#evaluate colless index (normalized with number of tips)
c = ts.relative("colless_index", rel = "TIPS")
#evaluate colless index (normalized with maximum value)
c = ts.relative("colless_index", rel = "MAX")
#evaluate colless index (normalized with expected value under the yule model)
c = ts.relative("colless_index", rel = "YULE")

#evaluate absolute values for all indices
#returns a dict with indices as keys
#if the index is not defined for the input tree, the respective entriy is nan
res = ts.all_absolute()
print(res["colless_index"])
#evaluate relative values (normalized by number of tips) for all indices
#also possible for the other normalization approaches
#returns a dict with indices as keys
#if the index is not defined for the input tree, the respective entriy is nan
res = ts.all_relative(rel = "TIPS")

# evaluation for the 10 indices with minimum pairwise spearman rank correlation based on our experiments
# possible for k = 2,..,10
res = ts.subset_absolute(k = 10)

#Evaluating indices for all possible positions of the root
t = Tree("example_unrooted.tree")
ats = AllRootTreeShape(t, mode = "BINARY", rooted = True)

#each of the following functions resturn dictionaries, in which the keys correspond to the possible root positions
#for the external branches, that is the name of the incident leaf, the internal branches are labeled with integer numbers

#dictionary of the corresponding rooted topologies
ats.all_rooted_trees
#dictionary of the absolute colless index values
res = ats.absolute("colless_index")
print(res["internal_0"])
#dictionary of the relative colless index values, normalized by the number of tips (analog for the other normalization options)
res = ats.relative("colless_index", "TIPS")
#dictionary of all defined absolute index values
res = ats.all_absolute()
print(res["internal_0"]["colless_index"])
#dictionary of all defined relative index values, normalized by the number of tips (analog for the other normalization options)
res = ats.all_relative(rel = "TIPS")
#dictionary of the absolute k index values with the minimum pairwise spearman rank correlation in our experiments
res = ats.subset_absolute(k = 10)

