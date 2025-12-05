"""
Design da árvore
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

class Visitor(ABC):
    """Classe abstrata para um Visitor
    """
    @abstractmethod
    def visit_decision_node(self, node: 'DecisionNode'):
        pass

    @abstractmethod
    def visit_leaf_node(self, node: 'LeafNode'):
        pass

class DepthVisitor(Visitor):
    """Visitor para calcular a profundidade da árvore
    """
    def __init__(self):
        self.current_depth = 0
    
    def visit_decision_node(self, node: 'DecisionNode'):
        print(f"Visitando nó de decisão")
        
    def visit_leaf_node(self, node: 'LeafNode'):
        print(f"Folha atingida")

class CountLeavesVisitor(Visitor):
    """Visitor para contar folhas

    """
    def __init__(self):
        self.leaf_count = 0
    
    def visit_decision_node(self, node: 'DecisionNode'):
        print("Visitando nó de decisão para contagem de folhas.")
        
    def visit_leaf_node(self, node: 'LeafNode'):
        self.leaf_count += 1
        print(f"Folha encontrada. Contagem de folhas: {self.leaf_count}")


class Node(ABC):
    """Uma classe abstrata para um nó
    """
    def __init__(self, parent: 'Node' = None):
        self.type = "GenericNode"
        self.parent = parent
        
    @abstractmethod
    def accept(self, visitor):
        pass
    
class DecisionNode(Node):
    """Nó de decisão que pode ter dois filhos
    """
    def __init__(self, parent: Optional['Node'] = None, left_child: Optional['Node'] = None, right_child: Optional['Node'] = None):
        super().__init__(parent)
        self.type = "DecisionNode"
        self.left_child = left_child
        self.right_child = right_child
        
    def add_child(self, child: 'Node'):
        if not self.left_child:
            self.add_left_child(child)
        elif not self.right_child:
            self.add_right_child(child)
        else:
            raise Exception("Both child nodes are already set.")
        
    def add_left_child(self, child: 'Node'):
        if not isinstance(child, Node):
            raise ValueError("Child must be an instance of Node.")
        
        if self.left_child is not None:
            raise Exception("Left child is already set.")
        self.left_child = child
        self.left_child.parent = self
    
    def add_right_child(self, child: 'Node'):
        if not isinstance(child, Node):
            raise ValueError("Child must be an instance of Node.")
        
        if self.right_child is not None:
            raise Exception("Right child is already set.")
        self.right_child = child
        self.right_child.parent = self
        
    def accept(self, visitor: Visitor):
        visitor.visit_decision_node(self)
    
    
class LeafNode(Node):
    """Nó folha que não tem filhos
    """
    def __init__(self, value: Any, parent: Optional['Node'] = None):
        super().__init__(parent)
        self.type = "LeafNode"
        self.value = value
        
    def accept(self, visitor: Visitor):
        visitor.visit_leaf_node(self)

class TreeBuilder:
    """Construtor de árvore
    """
    def __init__(self):
        self.root = None
        self.state = None
        
    def set_state(self, state: Optional['State']):
        self.state = state
        
    def run_step(self):
        if self.state:
            print("Estado atual:", type(self.state).__name__)
            self.state.handle(self)
        else:
            print("Nenhum estado definido para o construtor.")
        
    def build_tree(self):
        self.set_state(SplittingState())
        self.run_step()
        self.set_state(StoppingState())
        self.run_step()
        self.set_state(PruningState())
        self.run_step()
        
        
class State(ABC):
    """Uma classe abstrata para um estado
    """
    @abstractmethod
    def handle(self, builder):
        pass

class SplittingState(State):
    """Estado que lida com a divisão dos nós
    """
    def __init__(self):
        self.new_leaf_count = 0
        
    def _make_split(self, node: Node):
        if isinstance(node, DecisionNode):
            if node.left_child is None:
                self.new_leaf_count += 1
                node.left_child = LeafNode(value=f"{self.new_leaf_count:02d}", parent=node)
            else:
                self._make_split(node.left_child)
            if node.right_child is None:
                self.new_leaf_count += 1
                node.right_child = LeafNode(value=f"{self.new_leaf_count:02d}", parent=node)
            else:
                self._make_split(node.right_child)
        
    def handle(self, builder: TreeBuilder):
        if builder.root is None:
            builder.root = DecisionNode()
            print("Criada a raiz da árvore como um nó de decisão.")
            
        self._make_split(builder.root)
        print("Handling splitting state.")
        

class StoppingState(State):
    """Estado que lida com a parada da divisão
    """
    def handle(self, builder: TreeBuilder):
        print("Handling stopping state.")

class PruningState(State):
    """Estado que lida com a poda da árvore
    """
    def handle(self, builder: TreeBuilder):
        print("Handling pruning state.")
        
class Iterator(ABC):
    """Uma classe abstrata para um iterador
    """
    
    def __init__(self, root):
        if root is None:
            print("Aviso: A raiz é None.")
        elif not isinstance(root, Node):
            raise ValueError("Root must be an instance of Node.")
        
        self.root = root
        self.stack = [root] if root else []
    
    def __iter__(self):
        return self
    
    @abstractmethod
    def __next__(self):
        pass
    
class PreOrderIterator(Iterator):
    """Iterador para percorrer a árvore em pré-ordem (DFS)

    """
        
    def __next__(self):
        if not self.stack:
            raise StopIteration
        
        current_node = self.stack.pop()
        if isinstance(current_node, DecisionNode):
            if current_node.right_child:
                self.stack.append(current_node.right_child)
            if current_node.left_child:
                self.stack.append(current_node.left_child)
        
        return current_node