import unittest
import random
from functools import reduce
from typing import Callable
import argparse
from calc import mathEval
from math import cos, sin, tan, log as ln, log10 as log
import math
import time
import asyncio
from threading import Thread
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

csc = lambda x: 1 / sin(x)
sec = lambda x: 1 / cos(x)
cot = lambda x: 1 / tan(x)


class buildWorker(Thread):
    def __init__(self, task: Queue, output: Queue) -> None:
        Thread.__init__(self)
        self.task = task
        self.output = output

    def run(self):
        while True:
            func, correct, depth = self.task.get()
            self.output.put(func(correct, depth))
            self.task.task_done()


class testCaseGenerator:
    def __init__(self, length: int, correct: bool) -> None:
        self.length = length
        self.correct = correct
        self.MAX_DEPTH = 6
        self.syntax_matrix_index = {
            "NUM": 0,
            "PLUS": 1,
            "MINUS": 2,
            "MULT": 3,
            "DIV": 4,
            "EXP": 5,
            "SIN": 6,
            "COS": 7,
            "TAN": 8,
            "CSC": 9,
            "SEC": 10,
            "COT": 11,
            "LN": 12,
            "LOG": 13,
            "UMINUS": 14,
            "UPLUS": 15,
            "PAR": 16,
            "CURL": 17,
            "END": 18,
            "START": 19,
        }
        self.nesting_tokens = ["SIN", "COS", "TAN", "CSC", "SEC", "COT", "LN", "LOG", "PAR", "CURL"]
        self.syntax_matrix = [
            # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # NUM 0
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # PLUS 1
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # MINUS 2
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # MULT 3
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # DIV 4
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # EXP 5
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # SIN 6
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # COS 7
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # TAN 8
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # CSC 9
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # SEC 10
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # COT 11
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # LN 12
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # LOG 13
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],  # UMINUS 14
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],  # UPLUS 15
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # PAR 16
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # CURL 17
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # END 18
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # START 19
        ]
        self.expressions: list[list[str]] = []
        self.MAX_LENGTH = 100
        task1 = lambda correct, d, l: self.buildExpr(correct, d, l)
        executor1 = ThreadPoolExecutor(max_workers=16)
        self.expressions = list(
            executor1.map(
                task1,
                [correct for i in range(length)],
                [0 for i in range(length)],
                [0 for i in range(length)],
            )
        )
        task2 = lambda expr: list(map(
            lambda token: str((random.random() * 2 - 1) * 100000.0) if token == "NUM" else token,
            expr,
        ))
        executor2 = ThreadPoolExecutor(max_workers=16)
        self.expressions = list(
            executor2.map(
                task2,
                self.expressions,
            )
        )

    def buildExpr(self, correct, depth, totallen: int) -> "list[str]":
        prevToken = "START"
        names = list(self.syntax_matrix_index.keys())
        expression: list[str] = []
        while prevToken != "END":
            if not correct and max(totallen, len(expression)) > 10:
                prevToken = random.choice(names)
                if prevToken == "END":
                    break
            possibleChoices: list[int] = list(
                map(
                    lambda x: x[0],
                    filter(
                        lambda x: x[1] > 0,
                        enumerate(self.syntax_matrix[self.syntax_matrix_index[prevToken]]),
                    ),
                )
            )
            nextToken = names[random.choice(possibleChoices)]

            hasEnd = self.syntax_matrix_index["END"] in map(
                lambda x: x[0],
                filter(
                    lambda x: x[1] > 0,
                    enumerate(self.syntax_matrix[self.syntax_matrix_index[prevToken]]),
                ),
            )
            if (
                len(expression) >= self.MAX_LENGTH or depth >= self.MAX_DEPTH
            ) and hasEnd:
                nextToken = "END"

            if nextToken in self.nesting_tokens:
                bracetype = nextToken
                if nextToken not in ["PAR", "CURL"]:
                    expression.append(nextToken)
                    bracetype = "PAR"
                expression.append("L" + bracetype)
                expression.extend(self.buildExpr(correct, depth + 1, totallen + len(expression)))
                expression.append("R" + bracetype)
            else:
                expression.append(nextToken)

            prevToken = nextToken

        return expression

    def getExpressions(self, tokenMap: "dict[str,Callable[[],str]]") -> "list[str]":
        def getTokenSymbol(token):
            if token in tokenMap.keys():
                return tokenMap[token]()
            else:
                return token

        expressions: list[str] = [
            reduce(lambda a, b: a + b, map(getTokenSymbol, expression))
            for expression in self.expressions
        ]
        return expressions

    def __len__(self):
        return self.length


caclulatorTokenMap = {
    "PLUS": lambda: "+",
    "MINUS": lambda: "-",
    "MULT": lambda: "*",
    "DIV": lambda: "/",
    "EXP": lambda: "^",
    "SIN": lambda: "sin",
    "COS": lambda: "cos",
    "TAN": lambda: "tan",
    "CSC": lambda: "csc",
    "SEC": lambda: "sec",
    "COT": lambda: "cot",
    "LN": lambda: "ln",
    "LOG": lambda: "log",
    "UMINUS": lambda: "-",
    "UPLUS": lambda: "+",
    "LPAR": lambda: "(",
    "RPAR": lambda: ")",
    "LCURL": lambda: "(",  # ignore curly braces
    "RCURL": lambda: ")",
    "END": lambda: "",
    "START": lambda: "",
}
oracleTokenMap = {
    "PLUS": lambda: "+",
    "MINUS": lambda: "-",
    "MULT": lambda: "*",
    "DIV": lambda: "/",
    "EXP": lambda: "**",
    "SIN": lambda: "sin",
    "COS": lambda: "cos",
    "TAN": lambda: "tan",
    "CSC": lambda: "csc",
    "SEC": lambda: "sec",
    "COT": lambda: "cot",
    "LN": lambda: "ln",
    "LOG": lambda: "log",
    "UMINUS": lambda: "-",
    "UPLUS": lambda: "+",
    "LPAR": lambda: "(",
    "RPAR": lambda: ")",
    "LCURL": lambda: "(",  # ignore curly braces
    "RCURL": lambda: ")",
    "END": lambda: "",
    "START": lambda: "",
}


def oracle(expr):
    try:
        return eval(expr)
    except Exception as e:
        return e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Calculator Test",
        description="Tests the calculator with mathematical expressions",
        epilog="by Ahmad Izzuddin",
    )
    parser.add_argument(
        "-nc", "--ncases", dest="ncases", action="store", required=True, default=500
    )
    args = parser.parse_args()

    correct = testCaseGenerator(int(args.ncases), True)
    oracleCorrect = correct.getExpressions(oracleTokenMap)
    calcCorrect = correct.getExpressions(caclulatorTokenMap)
    incorrect = testCaseGenerator(int(args.ncases), False)
    oracleIncorrect = incorrect.getExpressions(oracleTokenMap)
    calcIncorrect = incorrect.getExpressions(caclulatorTokenMap)
    OCresult = list(map(lambda x: oracle(x), oracleCorrect))
    OIresult = list(map(lambda x: oracle(x), oracleIncorrect))
    CCresult = list(map(lambda x: mathEval(x), calcCorrect))
    CIresult = list(map(lambda x: mathEval(x), calcIncorrect))
    actualCorrect = list(
        filter(lambda x: type(x[0]) == float, zip(OCresult, CCresult, calcCorrect))
    )
    truePos = 0
    trueNeg = 0
    falsePos = 0
    falseNeg = 0

    print("Correct Results")
    print(f'|{"No.":4}|{"Expression":50}|{"isequal":7}|{"Oracle":10}|{"Calculator":10}|')
    for i, [Ores, Cres, expr] in enumerate(actualCorrect):
        if type(Cres) == float and type(Ores) == float:
            isequal = math.isclose(Ores, Cres, rel_tol=0.0001)
            truePos += 1
        else:
            isequal = False
            falseNeg += 1
        print(
            f"|{i:4}|{expr[1:min(len(expr),50)]:50}|{isequal:7}|{str(Ores)[1:min(len(expr),10)]:10}|{str(Cres)[1:min(len(expr),10)]:10}|"
        )

    notActualCorrect = list(
        filter(lambda x: type(x[0]) != float, zip(OCresult, CCresult, calcCorrect))
    )
    print("Incorrect Results")
    print(f'|{"No.":4}|{"Expression":50}|{"Oracle":10}|{"Calculator":10}|')
    for i, [Ores, Cres, expr] in enumerate(
        notActualCorrect + list(zip(OIresult, CIresult, oracleIncorrect))
    ):
        if type(Cres) == float:
            falsePos += 1
        else:
            trueNeg += 1
        print(
            f"|{i:4}|{expr[1:min(len(expr),50)]:50}|{str(Ores)[1:min(len(expr),10)]:10}|{str(Cres)[1:min(len(expr),10)]:10}|"
        )
    print("-" * 80)
    accuracy = (truePos + trueNeg) / (truePos + trueNeg + falseNeg + falsePos)
    recall = (truePos + falsePos) / (truePos + trueNeg + falseNeg + falsePos)
    print("Statistics")
    print(f"|{truePos=:10}|{trueNeg=:10}|{falsePos=:10}|{falseNeg=:10}|")
    print(f"|{accuracy=:10f}|{recall=:10f}")
