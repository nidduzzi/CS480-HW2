from math import cos, log, log10, sin, tan
from mathError import MathComputeError, MathError
from node import Node, NodeClass, NodeType

# -------------------------------------------------------------------------------------
# Credits:
# Based of work from https://github.com/gnebehay/parser

class MathCompute:
    def __init__(self):
        self.operations = {
            NodeType.T_PLUS: lambda a, b: a+b,
            NodeType.T_MINUS: lambda a, b: a-b,
            NodeType.T_MULT: lambda a, b: a*b,
            NodeType.T_DIV: lambda a, b: a/b,
            NodeType.T_EXP: lambda a, b: a**b,
            NodeType.T_SIN: lambda x: sin(x),
            NodeType.T_COS: lambda x: cos(x),
            NodeType.T_TAN: lambda x: tan(x),
            NodeType.T_CSC: lambda x: 1/sin(x),
            NodeType.T_SEC: lambda x: 1/cos(x),
            NodeType.T_COT: lambda x: 1/tan(x),
            NodeType.T_LN: lambda x: log(x),
            NodeType.T_LOG: lambda x: log10(x),
            NodeType.T_UMINUS: lambda x: -x,
            NodeType.T_UPLUS: lambda x: x,
        }

    def compute(self, node: Node) -> float:
        if node.node_class == NodeClass.NUM:
            return node.value
        elif node.node_class == NodeClass.UNARY:
            operation = self.operations[node.node_type]
            try:
                return operation(self.compute(node.children[0]))
            except MathError as e:
                raise e
            except Exception as e:
                raise MathComputeError(
                    node.tokenizer.inputString, node.span, 'Computation Error: ' + str(e))
        elif node.node_class == NodeClass.BINARY:
            left_result = self.compute(node.children[0])
            right_result = self.compute(node.children[1])
            operation = self.operations[node.node_type]
            try:
                return operation(left_result, right_result)
            except MathError as e:
                raise e
            except Exception as e:
                raise MathComputeError(
                    node.tokenizer.inputString, node.span, 'Computation Error: ' + str(e))
        else:
            raise MathComputeError(node.tokenizer.inputString, node.span,
                                   "Computation Error: invalid node class {} in computation".format(node.node_class))

# -------------------------------------------------------------------------------------
