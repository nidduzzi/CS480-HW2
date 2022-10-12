from copy import copy, deepcopy
import re
from typing import List
from mathTokenizer import MathTokenizer
from node import Node, NodeType


class MathParser():
    def __init__(self, inputString: str) -> None:
        self.lexer = MathTokenizer(inputString)
        self.inputString = inputString
        self.tokens = deepcopy(self.lexer.c_tokens)
        self.i = 0
        self.len = len(self.tokens)
        self.ast: Node
        self.parse_experession()
    # Util functions

    def print(self, ttype=False, ntype=True, v=True):
        self.ast.print(ttype=ttype, ntype=ntype, v=v)

    def currentToken(self):
        return self.lexer.c_tokens[self.i]

    def next(self):
        if self.i < self.len:
            self.i += 1

    def parse_experession(self):
        self.ast = self.parse_expression_precedence(0)
        self.match(NodeType.T_END)

    def parse_expression_precedence(self, precedence: int):
        if precedence == 0:
            left_node = self.parse_expression_precedence(1)

            while self.currentToken().node_type in [NodeType.T_PLUS, NodeType.T_MINUS]:
                node = self.currentToken()
                self.next()
                node.children.append(left_node)
                node.children.append(
                    self.parse_expression_precedence(1))
                left_node = node

            return left_node
        elif precedence == 1:
            left_node = self.parse_expression_precedence(2)

            while self.currentToken().node_type in [NodeType.T_MULT, NodeType.T_DIV]:
                node = self.currentToken()
                self.next()
                node.children.append(left_node)
                node.children.append(
                    self.parse_expression_precedence(2))
                left_node = node

            return left_node
        elif precedence == 2:
            left_node = self.parse_expression_precedence(3)

            while self.currentToken().node_type in [NodeType.T_EXP]:
                node = self.currentToken()
                self.next()
                node.children.append(
                    self.parse_expression_precedence(3))
                node.children.append(left_node)
                left_node = node

            return left_node
        elif precedence == 3:
            expression: Node
            ops = [NodeType.T_UPLUS, NodeType.T_UMINUS]
            if self.currentToken().node_type in ops:
                while self.currentToken().node_type in ops:
                    node = self.currentToken()
                    self.next()
                    node.children.append(
                        self.parse_expression_precedence(4))
                    expression = node
            else:
                expression = self.parse_expression_precedence(4)
            return expression
        elif precedence == 4:
            expression: Node
            ops = [NodeType.T_SIN, NodeType.T_COS,
                   NodeType.T_TAN, NodeType.T_COT, NodeType.T_LN, NodeType.T_LOG]
            if self.currentToken().node_type in ops:
                while self.currentToken().node_type in ops:
                    node = self.currentToken()
                    self.next()
                    node.children.append(
                        self.parse_expression_precedence(5))
                    expression = node
            else:
                expression = self.parse_expression_precedence(5)
            return expression
        elif precedence == 5:
            expression: Node
            if self.currentToken().node_type == NodeType.T_NUM:
                expression = self.currentToken()
                self.next()
                return expression
            if self.currentToken().node_type == NodeType.T_LCURL:
                self.match(NodeType.T_LCURL)
                expression = self.parse_expression_precedence(0)
                self.match(NodeType.T_RCURL)
            else:
                self.match(NodeType.T_LPAR)
                expression = self.parse_expression_precedence(0)
                self.match(NodeType.T_RPAR)
            return expression
        elif precedence == 6:
            left_node = self.parse_expression_precedence(7)
        elif precedence == 7:
            pass

    def match(self, ttype: NodeType):
        if self.currentToken().node_type == ttype:
            return self.next()
        else:
            raise Exception(
                'Invalid syntax: Expected token type {} on token {} of type {} at {}\ninput string: {}'.format(ttype, self.currentToken().value, self.currentToken().node_type, self.currentToken().span, self.inputString))


# def parse_e(tokens):
#     left_node = parse_e2(tokens)

#     while tokens[0].token_type in [TokenType.T_PLUS, TokenType.T_MINUS]:
#         node = tokens.pop(0)
#         node.children.append(left_node)
#         node.children.append(parse_e2(tokens))
#         left_node = node

#     return left_node


# def parse_e2(tokens):
#     left_node = parse_e3(tokens)

#     while tokens[0].token_type in [TokenType.T_MULT, TokenType.T_DIV]:
#         node = tokens.pop(0)
#         node.children.append(left_node)
#         node.children.append(parse_e3(tokens))
#         left_node = node

#     return left_node


# def parse_e3(tokens):
#     if tokens[0].token_type == TokenType.T_NUM:
#         return tokens.pop(0)

#     match(tokens, TokenType.T_LPAR)
#     expression = parse_e(tokens)
#     match(tokens, TokenType.T_RPAR)

#     return expression
