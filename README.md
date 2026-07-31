# treeshapy
![logo](https://raw.githubusercontent.com/luisevonderwiese/treeshapy/refs/heads/master/treeshapy_logo.png)
## Description
## Installation
```
pip install treeshapy
```
## Usage
Check out `example/example.py` to run the full example. <br><br>

List all implemented indices
```
import treeshapy
treeshapy.INDICES
```
Initialize the `TreeShape` object. <br>
```
from ete3 import Tree
from treeshapy import TreeShape

t = Tree("example_rooted.tree")
ts = TreeShape(t)
```
The input tree must exhibit unique leaf labels / taxon names. It is detected automatically, whether the tree is rooted/unrooted and binary/multifurcating. If you want to set these properties explicitly, use the boolean flags `rooted` and `binary`.<br>
The `TreeShape` object stores the `Tree` object internally and keeps index values and intermediate results as features of its nodes.<br><br>

Evaluation modes: <br>
|  `eval_mode` |   |
| ------ | ----- |
| `ABS` (default) | absolute                      |
| `REL_TIPS` | normalized by number of tips                      |
| `REL_MAX`  | normalized by maximum value                       |
| `REL_YULE` | normalized expected value under the Yule model |

Not all indices are defined for multifurcating or unrooted input trees or in the modes `REL_MAX` and `REL_YULE`. <br><br>

List available indices: <br>
```
ts.index_list() # indices available for evaluation of absolute values
ts.index_list("REL_MAX") # indices available for evaluation of values normalized by number of tips
```
List indices with minimum pariwise correlation (possible for binary rooted trees only):
```
ts.index_list(10) # 10 indices with minimum pairwise correlation
```
Evaluate a single index (here `"colless_index"`):
```
c = ts.evaluate("colless_index")
c_rel = ts.evaluate("colless_index", "REL_TIPS")
```
Evaluate multiple indices:
```
ts.evaluate("all") # evaluate absolute values of all available indices
ts.evaluate("all", "REL_TIPS") # evaluate values normalized by number of tips for all available indices
```
Evaluate indices with minimum pariwise correlation (possible for binary rooted trees only):
```
ts.evaluate(10)
```

### Unrooted Tree
```
t = Tree("example_unrooted.tree")
ts = TreeShape(t)
```
List all possible rooted trees:
```
ts.get_all_rooted_trees()
```
Evaluation for all possible rooted trees:
```
ts.evaluate_for_all_roots("colless_index")
ts.evaluate_for_all_roots("colless_index", "REL_TIPS")
ts.evaluate_for_all_roots("all")
ts.evaluate_for_all_roots("all", "REL_TIPS")
ts.evaluate_for_all_roots(10)
```

