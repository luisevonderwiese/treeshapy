# treeshapy Documentation

**treeshapy**

treeshapy is a Python  library for the evaluation of tree shape indices, based on the `Tree` object of `ete3`. 
56 topology-based indices are supported, combined with three normalization approaches
(normalization by number of tips, by maximum value and by expected value under the Yule model).
treeshapy has a particular focus on unrooted trees. Indices, which do not require a root can be evaluated for unrooted trees as well.
Additionally, there is a mode which offers the evaluation for all possible positions of the root.
With our [large-scale evaluation](some-link-to-add), we have determined subsets of indices with minimum pairwise correlation.
treeshapy offers a direct interface for evaluating such a subset on a given tree.

## Installation

Install the latest version from PyPI:

```bash
pip install treeshapy
```

For development, clone the repository and install it in editable mode:

```bash
git clone https://github.com/luisevonderwiese/treeshapy.git
cd treeshapy/
pip install -e .
```

## Quick start

```python
from ete3 import Tree

import treeshapy
from treeshapy import TreeShape

treeshapy.INDICES

t = Tree("example_rooted.tree")
ts = TreeShape(t)
ts.index_list()
ts.index_list("REL_MAX")
ts.index_list(10)

c = ts.evaluate("colless_index")
c_rel = ts.evaluate("colless_index", "REL_TIPS")

ts.evaluate("all")
ts.evaluate("all", "REL_TIPS")

ts.evaluate(10)

t = Tree("example_unrooted.tree")
ts = TreeShape(t)
ts.index_list("ABS")
ts.get_all_rooted_trees()

ts.evaluate("all")
ts.evaluate_for_all_roots("colless_index")
ts.evaluate_for_all_roots("all")
```

## Documentation

* **[API Reference](api.md)** - documentation of the main class `TreeShape`
* **[GitHub repository](https://github.com/luisevonderwiese/treeshapy)**

## Citation

If you use this software in your research, please cite:

> todo.*

## License

This project is released under the MIT License.

