from cmath import cos, log, log10, sin, tan
import sys
from typing import Dict, List

from graphvis import label, to_graphviz
from mathTokenizer import MathTokenizer
from node import Node, NodeClass, NodeType, TokenType


class TestCase:
    def __init__(self, inputString, tokens, tree, result):
        self.inputString = inputString
        self.tokens = tokens
        self.tree = tree
        self.result = result

    def testTokens(self, tokens):
        pass

    def testTree(self, tree):
        pass

    def testResult(self, result):
        pass


testCasesPass: Dict[str, TestCase] = {
    "1+1": TestCase("1+1", [Node(TokenType.T_NUM, (0, 1), node_type=NodeType.T_NUM, node_class=NodeClass.NUM, value=1.), Node(TokenType.T_PLUS, (1, 2), node_type=NodeType.T_PLUS, node_class=NodeClass.BINARY, value='+'), Node(TokenType.T_NUM, (2, 3), node_type=NodeType.T_NUM, node_class=NodeClass.NUM, value=1.)], Node(TokenType.T_PLUS, (1, 2)), 1+1),
    "1+-1": TestCase("1+-1", [], Node(TokenType.T_PLUS, (1, 2)), 1+-1),
    "-2": TestCase("-2", [], Node(TokenType.T_MINUS, (0, 1)), -2),
    "10.3432/2+SIN(3^5^5)": TestCase("10.3432/2+SIN(3^5^5)", [], Node(TokenType.T_PLUS, (9, 10)), 10.3432/2+sin(3**5)),
    "-4^SIN(-4)": TestCase("-4^SIN(-4)", [], Node(TokenType.T_EXP, (2, 3)), -4**sin(-4)),
    "0*5": TestCase("0*5", [], Node(TokenType.T_MULT, (1, 2)), 0*5),
    "LOG(1)+2": TestCase("LOG(1)+2", [], Node(TokenType.T_PLUS, (6, 7)), log10(1)+2),
    "LN(2)": TestCase("LN(2)", [], Node(TokenType.T_LN, (0, 2)), log(2)),
    "2*SIN(COS(TAN(COT(4))))*0.5": TestCase("2*SIN(COS(TAN(COT(4))))*0.5", [], Node(TokenType.T_MULT, (1, 2)), 2*sin(cos(tan(1/tan(4))))*0.5)
}


def testMathTokenizer(options, inputString=None):
    if inputString != None:
        mt = MathTokenizer(inputString)
        if 'p' in options:
            print(repr(mt.inputString))
            for t in mt.c_tokens:
                t.print(ttype=False, end=', ')
        if 'g' in options:
            label(mt.c_tokens)
            to_graphviz(mt.c_tokens, testCase=inputString,
                        png=('i' in options))
    else:
        passCount = 0
        mts: List[Dict[MathTokenizer, str]] = []
        for testCase in testCasesPass:
            mt = MathTokenizer(testCase)
            mts.append({"mt": mt, "testCase": testCase})
            # v flag for validate testcase
            if 'v' not in options:
                continue
            if testCasesPass[testCase].testTokens(mt.c_tokens):
                passCount += 1
        if 'p' in options:
            for mt in mts:
                print('test case: {}\ntokens: '.format(
                    mt["testCase"]))
                for t in mt["mt"].c_tokens:
                    t.print(ttype=False, end=', ')
                print('\n')

        if 'g' in options:
            for i, mt in enumerate(mts):
                label(mt["mt"].c_tokens)
                to_graphviz(mt["mt"].c_tokens, num=i,
                            testCase=mt["testCase"], png=('i' in options))


def testMathParser(options, inputString=None):
    pass


def testMathCompiler(options, inputString=None):
    pass


def testModules(moduleName: str, options, inputString=None):
    if moduleName == "MathTokenizer":
        testMathTokenizer(options, inputString)
    elif moduleName == "MathParser":
        testMathParser(options, inputString)
    elif moduleName == "MathCompiler":
        testMathCompiler(options, inputString)


mathModules = ["MathTokenizer", "MathParser", "MathCompiler"]


# python test.py <input string> <options> <modules>
# <input string>: any arithmatic operation between quotes
# <options>: starts with '--'
#           m       Test certain modules ["MathTokenizer", "MathParser", "MathCompiler"]
#           g       Create graphviz representation
#           i       Create images from graphvis (requires graphvis to be installed)
#           p       Print the contents of each node
# <modules>: any of ["MathTokenizer", "MathParser", "MathCompiler"] maximum 3, (only used if 'm' option flag is used)
if __name__ == '__main__':
    if '--' in sys.argv[1][0:2]:
        options = sys.argv[1]
        # check if testing for specific module
        if 'm' in options:
            n = len(sys.argv) - 2
            for i in range(n):
                testModules(sys.argv[i+2], options)
        else:
            for m in mathModules:
                testModules(m, options)
    elif len(sys.argv) > 2:
        inputstring = sys.argv[1]
        options = ''
        if '--' in sys.argv[2][0:2]:
            options = sys.argv[2]
        # check if testing for specific module
        if 'm' in options:
            n = len(sys.argv) - 3
            for i in range(n):
                testModules(sys.argv[i+3], options, inputString=inputstring)
        else:
            for m in mathModules:
                testModules(m, options, inputString=inputstring)
