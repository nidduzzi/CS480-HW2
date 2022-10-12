from copy import copy, deepcopy
import re
from typing import List
from mathTokenizer import MathTokenizer
from node import Node, TokenType


class MathParser(MathTokenizer):
    def __init__(self, inputString: str) -> None:
        super().__init__(inputString)
        self.inputString = inputString
        self.parse_experession(self.c_tokens)

    def parse_experession(self, tokens: List[Node]):
        self.tokens = deepcopy(tokens)
        self.ast = self.parse_expression_precedence(self.tokens, 0)
        self.match(self.tokens, TokenType.T_END)

    def parse_expression_precedence(self, tokens: List[Node], precedence: int):
        if precedence is 0:
            left_node = self.parse_expression_precedence(tokens, 1)

            while tokens[0].token_type in [TokenType.T_PLUS, TokenType.T_MINUS]:
                node = tokens.pop(0)
                node.children.append(left_node)
                node.children.append(
                    self.parse_expression_precedence(tokens, 1))
                left_node = node

            return left_node
        elif precedence is 1:
            left_node = self.parse_expression_precedence(tokens, 2)

            while tokens[0].token_type in [TokenType.T_MULT, TokenType.T_DIV]:
                node = tokens.pop(0)
                node.children.append(left_node)
                node.children.append(
                    self.parse_expression_precedence(tokens, 2))
                left_node = node

            return left_node
        elif precedence is 2:
            left_node = self.parse_expression_precedence(tokens, 3)

            while tokens[0].token_type in [TokenType.T_EXP]:
                node = tokens.pop(0)
                node.children.append(left_node)
                node.children.append(
                    self.parse_expression_precedence(tokens, 3))
                left_node = node

            return left_node
        elif precedence is 3:
            # unary neg here?
            while tokens[0].token_type in [TokenType.T_SIN, TokenType.T_COS, TokenType.T_TAN, TokenType.T_COT, TokenType.T_LN, TokenType.T_LOG]:
                node = tokens.pop(0)
                node.children.append(
                    self.parse_expression_precedence(tokens, 4))
                left_node = node

            return left_node
        elif precedence is 4:
            left_node = self.parse_expression_precedence(tokens, 5)
            if tokens[0].token_type == TokenType.T_NUM:
                return tokens.pop(0)
            if tokens[0].token_type == TokenType.T_LCURL:
                self.match(tokens, TokenType.T_LCURL)
                expression = self.parse_expression_precedence(tokens, 0)
                self.match(tokens, TokenType.T_RCURL)
            else:
                self.match(tokens, TokenType.T_LPAR)
                expression = self.parse_expression_precedence(tokens, 0)
                self.match(tokens, TokenType.T_RPAR)
            return expression
        elif precedence is 5:
            left_node = self.parse_expression_precedence(tokens, 6)
        elif precedence is 6:
            left_node = self.parse_expression_precedence(tokens, 7)
        elif precedence is 7:
            pass

    def match(self, tokens: List[Node], token: TokenType):
        if tokens[0].token_type == token:
            return tokens.pop(0)
        else:
            raise Exception(
                'Invalid syntax on token {} at {}'.format(tokens[0].token_type, tokens[0].span))


def parse_e(tokens):
    left_node = parse_e2(tokens)

    while tokens[0].token_type in [TokenType.T_PLUS, TokenType.T_MINUS]:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e2(tokens))
        left_node = node

    return left_node


def parse_e2(tokens):
    left_node = parse_e3(tokens)

    while tokens[0].token_type in [TokenType.T_MULT, TokenType.T_DIV]:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e3(tokens))
        left_node = node

    return left_node


def parse_e3(tokens):
    if tokens[0].token_type == TokenType.T_NUM:
        return tokens.pop(0)

    match(tokens, TokenType.T_LPAR)
    expression = parse_e(tokens)
    match(tokens, TokenType.T_RPAR)

    return expression
