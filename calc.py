import sys
from mathCompute import MathCompute
from mathError import MathComputeError, MathError, MathParserError, MathTokenizerError
from mathParser import MathParser


def repl(mc=MathCompute()):
    try:
        while True:
            ans = None
            expression = input('> ')
            if expression == 'exit()' or expression == 'exit' or expression == 'off':
                return
            ans = mathEval(expression, mc)
            if type(ans) is float:
                print(ans)
            elif type(ans) in [MathError, MathComputeError, MathParserError, MathTokenizerError]:
                print("Error:")
                for i in ans.args[0]:
                    print('{}: {}'.format(i, ans.args[0][i]))
            else:
                print(
                    'Internal Error: unknown evluated expression result {}'.format(type(ans)))
    except EOFError:
        return


def mathEval(expression, mc=MathCompute()):
    ans = None
    try:
        mp = MathParser(expression)
        ans = mc.compute(mp.ast)
    except MathError as e:
        ans = e
    return ans

# python calc.py <options> <expressions>
# <options>:      start with "--" and add flags right after
#                 e    evaluate expressions given after the options (max 100 expressions)
#                 r    start "REPL"
# <expressions>:  mathematical expression to be evaluated in quotation marks max 100 in a row separated by space, the rest are not evaluated (only used if \"e\" option flag is given)

if __name__ == '__main__':
    helpstr = 'python calc.py <options> <expressions>\n<options>:      start with "--" and add flags right after\n                e    evaluate expressions given after the options (max 100 expressions)\n                r    start "REPL"\n<expressions>:  mathematical expression to be evaluated in quotation marks max 100 in a row separated by space, the rest are not evaluated (only used if \"e\" option flag is given)\n'
    mc = MathCompute()
    if len(sys.argv) > 1:
        if '--' in sys.argv[1][0:2]:
            options = sys.argv[1][2:]
            if 'e' in options:
                expressions = sys.argv[2:102]
                for i, expression in enumerate(expressions):
                    ans = mathEval(expression, mc)
                    if type(ans) is float:
                        print('#{} {} = {}'.format(i, expression, ans))
                    elif type(ans) in [MathError, MathComputeError, MathParserError, MathTokenizerError]:
                        print("Error:")
                        for i in ans.args[0]:
                            print('{}: {}'.format(i, ans.args[0][i]))
                    else:
                        print(
                            'Internal Error: unknown evluated expression result {}'.format(type(ans)))
            if 'r' in options:
                repl(mc)
    else:
        print(helpstr)
