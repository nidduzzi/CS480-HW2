from ast import operator
from node import Node, TokenType


class MathCompiler:
    def __init__(self):
        self.operations = {
            TokenType.T_PLUS: operator.add,
            TokenType.T_MINUS: operator.sub,
            TokenType.T_MULT: operator.mul,
            TokenType.T_DIV: operator.truediv
        }

    def compute(self, node: Node):
        if node.token_type == TokenType.T_NUM:
            return node.value
        left_result = self.compute(node.children[0])
        right_result = self.compute(node.children[1])
        operation = self.operations[node.token_type]
        return operation(left_result, right_result)
