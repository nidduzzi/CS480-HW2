from math import cos, log, log10, sin, tan
import sys
from typing import Dict, List, Set, TypedDict, Union

from graphvis import label, to_graphviz
from mathCompute import MathCompute
from mathError import MathError
from mathParser import MathParser
from mathTokenizer import MathTokenizer
from node import Node, NodeClass, NodeType, TokenType


class TestCase:
    def __init__(self, inputString: str, tokens: List[Node], tree: Node, result: float):
        self.inputString = inputString
        self.tokens = tokens
        self.tree = tree
        self.result = result

    def __str__(self) -> str:
        return self.inputString

    # TODO! add testcase validation
    def testTokens(self, tokens):
        pass

    def testTree(self, tree):
        pass

    def testResult(self, result):
        pass


# TODO! add testcase expected results
testCasesPass: Set[TestCase] = {
    TestCase("1+1", [
        Node(token_type=TokenType.T_NUM, span=(0, 1),
             node_type=NodeType.T_NUM, node_class=NodeClass.NUM, value=1.),
        Node(token_type=TokenType.T_PLUS, span=(1, 2),
             node_type=NodeType.T_PLUS, node_class=NodeClass.BINARY, value='+'),
        Node(token_type=TokenType.T_NUM, span=(2, 3),
             node_type=NodeType.T_NUM, node_class=NodeClass.NUM, value=1.)
    ],
        Node(token_type=TokenType.T_PLUS, span=(1, 2)), 1+1),
    TestCase("1+-1", [], Node(token_type=TokenType.T_PLUS,
             span=(1, 2)), 1+-1),
    TestCase("-2", [], Node(token_type=TokenType.T_MINUS, span=(0, 1)), -2),
    TestCase("10.3432/2+SIN(3^(5^5))", [],
             Node(token_type=TokenType.T_PLUS, span=(9, 10)), 10.3432/2+sin(3**5)),
    TestCase("-4^SIN(-4)", [], Node(token_type=TokenType.T_EXP,
             span=(2, 3)), -4**sin(-4)),
    TestCase("0*5", [], Node(token_type=TokenType.T_MULT, span=(1, 2)), 0*5),
    TestCase("LOG(1)+2", [], Node(token_type=TokenType.T_PLUS,
             span=(6, 7)), log10(1)+2),
    TestCase("LN(2)", [], Node(
        token_type=TokenType.T_LN, span=(0, 2)), log(2)),
    TestCase("2*SIN(COS(TAN(COT(4))))*0.5", [],
             Node(token_type=TokenType.T_MULT, span=(1, 2)), 2*sin(cos(tan(1/tan(4))))*0.5),
    TestCase("10^ln(cot(2/{3+sin(2)+2}))", [],
             Node(token_type=TokenType.T_EXP, span=(2, 3)), 10**log(1/tan(2/(3+sin(2)+2))))
}


def testMathTokenizer(options, inputString=None):
    # test with input from user
    if inputString != None:
        try:
            # tokenize input string
            mt = MathTokenizer(inputString)
            # print in terminal the result
            if 'p' in options:
                print(repr(mt.inputString))
                mt.print(end=', ')
            # create graphviz of tokens
            if 'g' in options:
                label(mt.c_tokens)
                to_graphviz(mt.c_tokens, testCase=inputString,
                            png=('i' in options))
        except MathError as e:
            print(e)
    # test with testcases
    else:
        class TestCaseResult(TypedDict):
            mt: Union[MathTokenizer, None]
            testCase: TestCase
            e: Union[MathError, None]
        passCount = 0
        mtrs: List[TestCaseResult] = []
        # test module with each testcase
        for testCase in testCasesPass:
            try:
                mt = MathTokenizer(testCase.inputString)
                mtrs.append({"mt": mt, "testCase": testCase})
                # v flag for validating module result with expected testcase result
                if 'v' not in options:
                    continue
                if testCase.testTokens(mt.c_tokens):
                    passCount += 1
            except MathError as e:
                mtrs.append({'e': e})
        # print testcase results
        if 'p' in options:
            for i, mtr in enumerate(mtrs):
                if 'e' in mtr:
                    print('#{} Error: {}'.format(i, mtr['e']))
                    continue
                print('#{} test case: {}\ntokens: '.format(
                    i, mtr["testCase"].inputString))
                mtr["mt"].print(end=', ')
        # create graphvis of testcase tokens
        if 'g' in options:
            for i, mtr in enumerate(mtrs):
                if 'e' in mtr:
                    continue
                label(mtr["mt"].c_tokens)
                to_graphviz(mtr["mt"].c_tokens, num=i,
                            testCase=mtr["testCase"].inputString, png=('i' in options))


def testMathParser(options, inputString=None):
    # test with input from user
    if inputString != None:
        try:
            mp = MathParser(inputString)
            if 'p' in options:
                print(repr(mp.inputString))
                mp.print()
            if 'g' in options:
                label(mp.ast)
                to_graphviz(mp.ast, testCase=inputString,
                            png=('i' in options))
        except MathError as e:
            print('Error: {}'.format(e))
    # test with testcases
    else:
        class TestCaseResult(TypedDict):
            mp: Union[MathParser, None]
            testCase: TestCase
            e: Union[MathError, None]
        passCount = 0
        mprs: List[TestCaseResult] = []
        for testCase in testCasesPass:
            try:
                mp = MathParser(testCase.inputString)
                mprs.append({"mp": mp, "testCase": testCase})
                # v flag for validate testcase
                if 'v' not in options:
                    continue
                if testCase.testTree(mp.ast):
                    passCount += 1
            except MathError as e:
                mprs.append({'e': e})
        # print testcase results
        if 'p' in options:
            for i, mpr in enumerate(mprs):
                if 'e' in mpr:
                    print('#{} Error: {}'.format(i, mpr['e']))
                    continue
                print('#{} test case: {}\ntokens: '.format(
                    i, mpr["testCase"].inputString))
                mpr["mp"].print()
        # create graphviz for testcase
        if 'g' in options:
            for i, mpr in enumerate(mprs):
                if 'e' in mpr:
                    continue
                label(mpr["mp"].ast)
                to_graphviz(mpr["mp"].ast, num=i,
                            testCase=mpr["testCase"].inputString, png=('i' in options))


def testMathCompiler(options, inputString=None):
    # test with input from user
    if inputString != None:
        try:
            mp = MathParser(inputString)
            mc = MathCompute()
            y = mc.compute(mp.ast)
            if 'p' in options:
                print(repr(mp.inputString))
                print('= {}'.format(y))
                mp.print()
            if 'g' in options:
                nodes = [Node(value=y), mp.ast]
                label(nodes)
                to_graphviz(nodes, testCase=inputString,
                            png=('i' in options))
        except MathError as e:
            print(e)
    # test with testcases
    else:
        class TestCaseResult(TypedDict):
            mp: Union[MathParser, None]
            y: Union[float, None]
            testCase: TestCase
            e: Union[MathError, None]
        passCount = 0
        mc = MathCompute()
        mcrs: List[TestCaseResult] = []
        for testCase in testCasesPass:
            try:
                mp = MathParser(testCase.inputString)
                y = mc.compute(mp.ast)
                mcrs.append({"mp": mp, "y": y, "testCase": testCase})
                # v flag for validate testcase
                if 'v' not in options:
                    continue
                if testCase.testResult(y):
                    passCount += 1
            except MathError as e:
                mcrs.append({'e': e})
        # print testcase results
        if 'p' in options:
            for i, mcr in enumerate(mcrs):
                if 'e' in mcr:
                    print('#{} Error: {}'.format(i, mcr['e']))
                    continue
                print('#{} test case: {} result: {}\ntokens: '.format(
                    i, mcr["testCase"].inputString, mcr['y']))
                mcr["mp"].print()
        # create graphviz for testcase
        if 'g' in options:
            for i, mcr in enumerate(mcrs):
                if 'e' in mcr:
                    continue
                nodes = [Node(value=y), mcr["mp"].ast]
                label(nodes)
                to_graphviz(nodes, num=i,
                            testCase=mcr["testCase"].inputString, png=('i' in options))


def testModules(moduleName: str, options, inputString=None):
    if moduleName == "MathTokenizer":
        testMathTokenizer(options, inputString)
    elif moduleName == "MathParser":
        testMathParser(options, inputString)
    elif moduleName == "MathCompute":
        testMathCompiler(options, inputString)
    else:
        print('{} is not a module, try one of {}'.format(moduleName, mathModules))


mathModules = ["MathTokenizer", "MathParser", "MathCompute"]


# python test.py <input string> <options> <modules>
# <input string>: any arithmatic operation between quotes
# <options>: starts with '--' and add flags after
#           m       Test certain modules ["MathTokenizer", "MathParser", "MathCompute"]
#           v       Verify results of testcases
#           g       Create graphviz representation
#           i       Create images from graphvis (requires graphvis to be installed)
#           p       Print the contents of each node
# <modules>: any of ["MathTokenizer", "MathParser", "MathCompute"] maximum 3, (only used if 'm' option flag is used)

if __name__ == '__main__':
    helpstr = 'python test.py <input string> <options> <modules>\n<input string>: any arithmatic operation between quotes\n<options>:      starts with "--" and add flags after\n                m       Test certain modules ["MathTokenizer", "MathParser", "MathCompute"]\n                v       Verify results of testcases\n                g       Create graphviz representation\n                i       Create images from graphvis (requires graphvis to be installed)\n                p       Print the contents of each node\n<modules>:      any of ["MathTokenizer", "MathParser", "MathCompute"] maximum 3 separated by space (only used if "m" option flag is used)'
    if len(sys.argv) > 1:
        if '--' in sys.argv[1][0:2]:
            options = sys.argv[1][2:]
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
                options = sys.argv[2][2:]
            # check if testing for specific module
            if 'm' in options:
                n = len(sys.argv) - 3
                for i in range(n):
                    testModules(sys.argv[i+3], options, inputString=inputstring)
            else:
                for m in mathModules:
                    testModules(m, options, inputString=inputstring)
    else:
        print(helpstr)
