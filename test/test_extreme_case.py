from ete3 import Tree
from treeshapy import TreeShape, INDICES

tree =  Tree("A;")
tb_b = TreeShape(tree, "BINARY")
tb_a = TreeShape(tree, "ARBITRARY")

for index_name in INDICES:
    print(index_name)
    try:
        print(tb_b.absolute(index_name))
    except ValueError as e:
        print(e)
    try:
        print(tb_a.absolute(index_name))
    except ValueError as e:
        print(e)
    try:
        print(tb_b.relative(index_name, "MAX"))
    except ValueError as e:
        print(e)
    try:
        print(tb_a.relative(index_name, "MAX"))
    except ValueError as e:
        print(e)
    try:
        print(tb_b.relative(index_name, "TIPS"))
    except ValueError as e:
        print(e)
    try:
        print(tb_a.relative(index_name, "TIPS"))
    except ValueError as e:
        print(e)

