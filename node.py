import enum
from re import Pattern
from typing import Callable, Dict, Tuple, TypedDict, Union


class TokenType(enum.Enum):
    T_NUM = 0
    T_PLUS = 1
    T_MINUS = 2
    T_MULT = 3
    T_DIV = 4
    T_EXP = 5
    T_SIN = 6
    T_COS = 7
    T_TAN = 8
    T_COT = 9
    T_LN = 10
    T_LOG = 11
    T_LPAR = 12
    T_RPAR = 13
    T_LCURL = 14
    T_RCURL = 15
    T_END = 16


tokenMappings: Dict[TokenType, Pattern] = {
    TokenType.T_NUM: r'(?:(?:[1-9]\d*)|0)(?:\.\d+)?',
    TokenType.T_PLUS: r'\+',
    TokenType.T_MINUS: r'\-',
    TokenType.T_MULT: r'\*',
    TokenType.T_DIV: r'\/',
    TokenType.T_EXP: r'\^',
    TokenType.T_LCURL: r'\{',
    TokenType.T_RCURL: r'\}',
    TokenType.T_SIN: r'(?:SIN)|(?:Sin)|(?:sin)',
    TokenType.T_COS: r'(?:COS)|(?:Cos)|(?:cos)',
    TokenType.T_TAN: r'(?:TAN)|(?:Tan)|(?:tan)',
    TokenType.T_COT: r'(?:COT)|(?:Cot)|(?:cot)',
    TokenType.T_LN: r'(?:LN)|(?:Ln)|(?:ln)',
    TokenType.T_LOG: r'(?:LOG)|(?:Log)|(?:log)',
    TokenType.T_LPAR: r'\(',
    TokenType.T_RPAR: r'\)',
}


class NodeType(enum.Enum):
    T_NUM = 0
    T_PLUS = 1
    T_MINUS = 2
    T_MULT = 3
    T_DIV = 4
    T_EXP = 5
    T_SIN = 6
    T_COS = 7
    T_TAN = 8
    T_COT = 9
    T_LN = 10
    T_LOG = 11
    T_UMINUS = 12
    T_UPLUS = 13
    T_LPAR = 14
    T_RPAR = 15
    T_LCURL = 16
    T_RCURL = 17
    T_END = 18


class NodeClass(enum.Enum):
    NUM = 0
    UNARY = 1
    BINARY = 2
    BRACKET = 3


class Node:
    def __init__(self, token_type: TokenType, span: Tuple[int, int], node_type: Union[NodeType, None] = None, node_class: Union[NodeClass, None] = None, value=None):
        self.token_type = token_type
        self.node_type = node_type
        self.node_class = node_class
        self.value = value
        self.children: list[Node] = []
        self.span = span
        self.id = -1
        self.__p_reset()

    def __p_reset(self):
        self.__p__ttype = False
        self.__p__ntype = True
        self.__p__v = True
        self.__p__span = True
        self.__p__end = '\n'

    # -------------------------------------------------------------------------------------
    # Modified from:
    # https://stackoverflow.com/questions/20242479/printing-a-tree-data-structure-in-python
    def __str__(self, level=0):
        ret = '\t'*level + '{ ' +\
            (('ttype: ' + repr(self.token_type)+(', 'if self.__p__ntype or self.__p__v or self.__p__span else ''))if self.__p__ttype else '') + \
            (('ntype: ' + repr(self.node_type)+(', 'if self.__p__v or self.__p__span else ''))if self.__p__ntype else '') + \
            (('v: ' + repr(self.value)+(', 'if self.__p__span else ''))if self.__p__v else '') + \
            (('s: ' + repr(self.span))if self.__p__span else '')+' }' + \
            ('' if (level == 0 and len(self.children) == 0)
             and not self.__p__end else '\n')
        for child in self.children:
            if type(child) is Node:
                ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'
    # -------------------------------------------------------------------------------------

    def print(self, ttype=False, ntype=True, v=True, span=True, end='\n'):
        self.__p__ttype = ttype
        self.__p__ntype = ntype
        self.__p__v = v
        self.__p__span = span
        self.__p__end = (end == '\n')
        print(self, end=end)
        self.__p_reset()

    def setPrecedence(self, precedence: int):
        self.precedence = precedence

    def setNodeClass(self, node_class: NodeClass):
        self.node_class = node_class

    def setNodeType(self, node_type: NodeType):
        self.node_type = node_type


class NodeChar(TypedDict):
    ttype: TokenType
    nclass: NodeClass
    isType: Callable[[TokenType, TokenType, TokenType], bool]


nodeMappings: Dict[NodeType, NodeChar] = {
    NodeType.T_NUM: {
        "ttype": TokenType.T_NUM,
        "nclass": NodeClass.NUM,
        "isType": lambda current, before, after: current is TokenType.T_NUM
    },
    NodeType.T_PLUS: {
        "ttype": TokenType.T_PLUS,
        "nclass": NodeClass.BINARY,
        "isType": lambda current, before, after: current is TokenType.T_PLUS and
        before in {TokenType.T_NUM, TokenType.T_RPAR, TokenType.T_RCURL} and
        after in {TokenType.T_NUM, TokenType.T_PLUS, TokenType.T_MINUS, TokenType.T_SIN, TokenType.T_COS,
                  TokenType.T_TAN, TokenType.T_COT, TokenType.T_LN, TokenType.T_LOG, TokenType.T_LPAR, TokenType.T_LCURL}
    },
    NodeType.T_MINUS: {
        "ttype": TokenType.T_MINUS,
        "nclass": NodeClass.BINARY,
        "isType": lambda current, before, after: current is TokenType.T_MINUS and
        before in {TokenType.T_NUM, TokenType.T_RPAR, TokenType.T_RCURL} and
        after in {TokenType.T_NUM, TokenType.T_PLUS, TokenType.T_MINUS, TokenType.T_SIN, TokenType.T_COS,
                  TokenType.T_TAN, TokenType.T_COT, TokenType.T_LN, TokenType.T_LOG, TokenType.T_LPAR, TokenType.T_LCURL}
    },
    NodeType.T_MULT: {
        "ttype": TokenType.T_MULT,
        "nclass": NodeClass.BINARY,
        "isType": lambda current, before, after: current is TokenType.T_MULT and
        before in {TokenType.T_NUM, TokenType.T_RPAR, TokenType.T_RCURL} and
        after in {TokenType.T_NUM, TokenType.T_PLUS, TokenType.T_MINUS, TokenType.T_SIN, TokenType.T_COS, TokenType.T_TAN,
                  TokenType.T_COT, TokenType.T_LN, TokenType.T_LOG, TokenType.T_LPAR, TokenType.T_LCURL}
    },
    NodeType.T_DIV: {
        "ttype": TokenType.T_DIV,
        "nclass": NodeClass.BINARY,
        "isType": lambda current, before, after: current is TokenType.T_DIV and
        before in {TokenType.T_NUM, TokenType.T_RPAR, TokenType.T_RCURL} and
        after in {TokenType.T_NUM, TokenType.T_PLUS, TokenType.T_MINUS, TokenType.T_SIN, TokenType.T_COS, TokenType.T_TAN,
                  TokenType.T_COT, TokenType.T_LN, TokenType.T_LOG, TokenType.T_LPAR, TokenType.T_LCURL}
    },
    NodeType.T_EXP: {
        "ttype": TokenType.T_EXP,
        "nclass": NodeClass.BINARY,
        "isType": lambda current, before, after: current is TokenType.T_EXP and
        before in {TokenType.T_NUM, TokenType.T_RPAR, TokenType.T_RCURL} and
        after in {TokenType.T_NUM, TokenType.T_SIN, TokenType.T_COS, TokenType.T_TAN,
                  TokenType.T_COT, TokenType.T_LN, TokenType.T_LOG, TokenType.T_LPAR, TokenType.T_LCURL}
    },
    NodeType.T_SIN: {
        "ttype": TokenType.T_SIN,
        "nclass": NodeClass.UNARY,
        "isType": lambda current, before, after: current is TokenType.T_SIN and
        after in {TokenType.T_NUM, TokenType.T_LPAR}
    },
    NodeType.T_COS: {
        "ttype": TokenType.T_COS,
        "nclass": NodeClass.UNARY,
        "isType": lambda current, before, after: current is TokenType.T_COS and
        after in {TokenType.T_NUM, TokenType.T_LPAR}
    },
    NodeType.T_TAN: {
        "ttype": TokenType.T_TAN,
        "nclass": NodeClass.UNARY,
        "isType": lambda current, before, after: current is TokenType.T_TAN and
        after in {TokenType.T_NUM, TokenType.T_LPAR}
    },
    NodeType.T_COT: {
        "ttype": TokenType.T_COT,
        "nclass": NodeClass.UNARY,
        "isType": lambda current, before, after: current is TokenType.T_COT and
        after in {TokenType.T_NUM, TokenType.T_LPAR}
    },
    NodeType.T_LN: {
        "ttype": TokenType.T_LN,
        "nclass": NodeClass.UNARY,
        "isType": lambda current, before, after: current is TokenType.T_LN and
        after in {TokenType.T_NUM, TokenType.T_LPAR}
    },
    NodeType.T_LOG: {
        "ttype": TokenType.T_LOG,
        "nclass": NodeClass.UNARY,
        "isType": lambda current, before, after: current is TokenType.T_LOG and
        after in {TokenType.T_NUM, TokenType.T_LPAR}
    },
    NodeType.T_UMINUS: {
        "ttype": TokenType.T_MINUS,
        "nclass": NodeClass.UNARY,
        "isType": lambda current, before, after: current is TokenType.T_MINUS and
        before in {None, TokenType.T_PLUS, TokenType.T_MINUS, TokenType.T_MULT, TokenType.T_DIV, TokenType.T_EXP, TokenType.T_SIN, TokenType.T_COS, TokenType.T_TAN, TokenType.T_COT, TokenType.T_LPAR, TokenType.T_LCURL} and
        after in {TokenType.T_NUM, TokenType.T_SIN, TokenType.T_COS, TokenType.T_TAN,
                  TokenType.T_COT, TokenType.T_LN, TokenType.T_LOG, TokenType.T_LPAR, TokenType.T_LCURL}
    },
    NodeType.T_UPLUS: {
        "ttype": TokenType.T_PLUS,
        "nclass": NodeClass.UNARY,
        "isType": lambda current, before, after: current is TokenType.T_PLUS and
        before in {None, TokenType.T_PLUS, TokenType.T_MINUS, TokenType.T_MULT, TokenType.T_DIV, TokenType.T_EXP, TokenType.T_SIN, TokenType.T_COS, TokenType.T_TAN, TokenType.T_COT, TokenType.T_LPAR, TokenType.T_LCURL} and
        after in {TokenType.T_NUM, TokenType.T_SIN, TokenType.T_COS, TokenType.T_TAN,
                  TokenType.T_COT, TokenType.T_LN, TokenType.T_LOG, TokenType.T_LPAR, TokenType.T_LCURL}
    },
    NodeType.T_LCURL: {
        "ttype": TokenType.T_LCURL,
        "nclass": NodeClass.BRACKET,
        "isType": lambda current, before, after: current is TokenType.T_LCURL and
        before in {None, TokenType.T_PLUS, TokenType.T_MINUS, TokenType.T_MULT, TokenType.T_DIV, TokenType.T_EXP, TokenType.T_LPAR, TokenType.T_LCURL} and
        after in {TokenType.T_NUM, TokenType.T_PLUS,
                  TokenType.T_MINUS, TokenType.T_SIN, TokenType.T_COS, TokenType.T_TAN, TokenType.T_COT, TokenType.T_LN, TokenType.T_LOG, TokenType.T_LPAR, TokenType.T_LCURL}
    },
    NodeType.T_RCURL: {
        "ttype": TokenType.T_RCURL,
        "nclass": NodeClass.BRACKET,
        "isType": lambda current, before, after: current is TokenType.T_RCURL and
        before in {TokenType.T_NUM, TokenType.T_RPAR, TokenType.T_RCURL} and
        after in {None, TokenType.T_PLUS, TokenType.T_MINUS, TokenType.T_MULT,
                  TokenType.T_DIV, TokenType.T_EXP, TokenType.T_RPAR, TokenType.T_RCURL}
    },
    NodeType.T_LPAR: {
        "ttype": TokenType.T_LPAR,
        "nclass": NodeClass.BRACKET,
        "isType": lambda current, before, after: current is TokenType.T_LPAR and
        before in {None, TokenType.T_PLUS, TokenType.T_MINUS, TokenType.T_MULT, TokenType.T_DIV, TokenType.T_EXP, TokenType.T_SIN, TokenType.T_COS, TokenType.T_TAN, TokenType.T_COT, TokenType.T_LN, TokenType.T_LOG, TokenType.T_LPAR, TokenType.T_LCURL} and
        after in {TokenType.T_NUM, TokenType.T_PLUS,
                  TokenType.T_MINUS, TokenType.T_SIN, TokenType.T_COS, TokenType.T_TAN, TokenType.T_COT, TokenType.T_LN, TokenType.T_LOG, TokenType.T_LPAR, TokenType.T_LCURL}
    },
    NodeType.T_RPAR: {
        "ttype": TokenType.T_RPAR,
        "nclass": NodeClass.BRACKET,
        "isType": lambda current, before, after: current is TokenType.T_RPAR and
        before in {TokenType.T_NUM, TokenType.T_RPAR, TokenType.T_RCURL} and
        after in {None, TokenType.T_PLUS, TokenType.T_MINUS, TokenType.T_MULT,
                  TokenType.T_DIV, TokenType.T_EXP, TokenType.T_RPAR, TokenType.T_RCURL}
    },
}
