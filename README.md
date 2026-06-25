# treeshapy
![logo](https://raw.githubusercontent.com/luisevonderwiese/treeshapy/refs/heads/master/treeshapy_logo.png)
## Description
## Requirements
## Installation
## Usage example
```
from ete3 import Tree

from treeshapy import treeshapy
from treeshapy.treeshapy import TreeShape
from treeshapy.all_root_treeshapy import AllRootTreeShape

#list of all implemented indices
print(treeshapy.INDICES)
#list of implemented indices defined for unrooted trees
print(treeshapy.INDICES_UNROOTED)

#read tree
t = Tree("example_rooted.nex")
#initialize treeshape object, set mode = "ARBITRARY" for a tree which is not binary
ts = TreeShape(t, mode = "BINARY", rooted = True)

#evaluate colless index (absolute)
c = ts.absolute("colless_index")
#evaluate colless index (normalized with number of tips)
c = ts.relative("colless_index", "TIPS")
#evaluate colless index (normalized with maximum value)
c = ts.relative("colless_index", "MAX")
#evaluate colless index (normalized with expected value under the yule model)
c = ts.relative("colless_index", "YULE")

#evaluate absolute values for all indices
#returns a dict with indices as keys
#if the index is not defined for the input tree, the respective entriy is nan
res = ts.all_absolute()
#evaluate relative values (normalized by number of tips) for all indices
#also possible for the other normalization approaches
#returns a dict with indices as keys
#if the index is not defined for the input tree, the respective entriy is nan
res = ts.all_relative("TIPS")

#Evaluating indices for all possible positions of the root
t = Tree("example_unrooted.nex")
ats = AllRootTreeShape(t, mode = "BINARY", rooted = True)

#each of the following functions resturn dictionaries, in which the keys correspond to the possible root positions
#for the external branches, that is the name of the incident leaf, the internal branches are labeled with integer numbers

#dictionary of the corresponding rooted topologies
ats.rooted_trees()
#dictionary of the absolute colless index values
ats.absolute("colless_index")
#dictionary of the relative colless index values, normalized by the number of tips (analog for the other normalization options)
ats.relative("colless_index", "TIPS")
#dictionary of all defined absolute index values
ats.all_absolute()
#dictionary of all defined relative index values, normalized by the number of tips (analog for the other normalization options)
ats.all_relative("TIPS")
```
## Implemented Tree Shape Indices
