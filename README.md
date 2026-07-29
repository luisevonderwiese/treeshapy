# treeshapy
![logo](https://raw.githubusercontent.com/luisevonderwiese/treeshapy/refs/heads/master/treeshapy_logo.png)
## Description
## Requirements
## Installation
## Usage
Check out `example/example.py` to run the full example
### Index Lists
List all implemented indices
```
import treeshapy
print(treeshapy.INDICES)
```
List indices implemented for unrooted trees
```
import treeshapy
print(treeshapy.INDICES_UNROOTED)
```
### The `TreeShape` Object
Initialize the `TreeShape` object. <br>
```
from ete3 import Tree
from treeshapy import TreeShape

t = Tree("example_rooted.tree")
ts = TreeShape(t, mode = "BINARY", rooted = True)
```
The input tree must exhibit unique leaf labels / taxon names. <br>
Use `mode = "BINARY"` for fully binary tree and `mode = "ARBITRARY"` for trees which may contain polytomies. <br>
The chosen mode affects the normalization. The `ARBITRARY` mode may hence also be used for binary trees if they are to be compared to non-binary trees.
Note that not all indices are defined for arbitrary trees (see [Implemented Indices](##Implemented-Indices)). <br>
Use `rooted = True` for rooted trees that are tree with an explicit binary root node.
Use `rooted = False` for unrooted trees. We expect the input tree to exhibit a toplevel trifurcation. If its toplevel node is binary, we assume that this is an implicit root and remove it. Please note that only the indices from `treeshapy.INDICES_UNROOTED` are defined for unrooted trees. <br>
The `TreeShape` object stores the `Tree`object internally and stores index values and intermediate results as features of its nodes.

### Evaluating a Single Index
As an example, we show the evaluation of the `colless_index`. All other tree shape indices from `treeshapy.INDICES` can be evaluated in the same way.
```
c = ts.absolute("colless_index")
c = ts.relative("colless_index", rel = "TIPS")
```
`rel` can be set to choose between different normalization techniques:
|  `rel = ` |  Normalization by |
| ------ | ----- |
| `TIPS` | number of tips                      |
| `MAX`  | maximum value                       |
| `YULE` | expected value under the Yule model |

Note that `MAX` and `YULE` are only defined for some indices (see [Implemented Indices](##Implemented-Indices)). The result of a normalization and whether it is defined can depend on the `mode` used to initialize the `TreeShape` object.

### Evaluating Multiple Indices
The following functions return a dictionary mapping the resulting values to the indices names. If an index is not defined, the entry is `nan`. <br>
Evaluating all (defined) indices:
```
res = ts.all_absolute()
print(res["colless_index"])
res = ts.all_relative("TIPS")
```
Evaluating a subset of `k` indices:
```
res = ts.subset_absolute(k = 10)
```
This is possible for `k = 2, ..., 10`. It evaluates the indices from a set of size `k` with minimum pairwise correlations. Such a set minimizes the sum of the pairwise Spearman rank correlations among all index sets of size `k` in our experiments. <br>
Using this option is highly recommended. Many indices exhibit high pairwise correlations. Evaluating all of them produced redundant results.

### The `AllRootTreeShape` object
Initialize the `AllRootTreeShape` object. <br>
```
from ete3 import Tree
from treeshapy import AllRootTreeShape

t = Tree("example_unrooted.tree")
ats = AllRootTreeShape(t, mode = "BINARY", rooted = True)
```
The input tree must exhibit unique leaf labels / taxon names. We handle the tree as unrooted, that is, we expect the input tree to exhibit a toplevel trifurcation. If its toplevel node is binary, we assume that this is an implicit root and remove it. We label the external branches with the name of the corresponding taxon. We enumerate the internal branches and assign labels `internal_x`. Subsequently, the tree is rooted at every possible branch. 

The following command returns a dictionary mapping each branch labels to the corresponding rooted topology:
```
ats.all_rooted_trees
```
### Evaluating indices with the The `AllRootTreeShape` object
Each of the following functions returns a dictionary, which assigns the values resulting for a rooted topology to the branch label of the branch on which the root is placed.
```
res = ats.absolute("colless_index")
print(res["internal_0"])
res = ats.relative("colless_index", rel = "TIPS")
```
The following functions return two-leveled dictionaries (branch label and index name)
```
res = ats.all_absolute()
print(res["internal_0"]["colless_index"])
res = ats.all_relative(rel = "TIPS")
res = ats.subset_absolute(k = 10)
```
## Implemented Tree Shape Indices
