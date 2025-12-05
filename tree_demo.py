from tree_design import TreeBuilder, PreOrderIterator, CountLeavesVisitor, DepthVisitor


# Constução da árvore de exemplo
builder = TreeBuilder()
builder.build_tree()


# Criação do iterador e visitantes
it = PreOrderIterator(builder.root)
depth_visitor = DepthVisitor()
leaf_visitor = CountLeavesVisitor()

# Itera e visita cada nó
for node in it:
    node.accept(depth_visitor)
    node.accept(leaf_visitor)
