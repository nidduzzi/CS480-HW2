import re
from typing import List, TypedDict
from node import Node, NodeType, TokenType, nodeMappings, tokenMappings


class MathTokenizer:
    def __init__(self, inputString: str):
        self.inputString = inputString
        self.c_tokens = self.tokenize(inputString)

    def print(self, ttype=False, ntype=True, v=True, end='\n'):
        for t in self.c_tokens:
            t.print(ttype=ttype, ntype=ntype, v=v, end=end)

    def tokenize(self, inputString: str) -> List[Node]:

        class RawToken(TypedDict):
            match: re.Match
            ttype: TokenType

        rawTokens: list[RawToken] = []
        # find all matching valid tokens
        for ttype in tokenMappings:
            for m in re.finditer(tokenMappings[ttype], inputString):
                if m != None:
                    rawTokens.append({"match": m, "ttype": ttype})
        # sort tokens by starting index
        rawTokens.sort(key=lambda tok: tok["match"].span()[0])

        i = 1
        hasOverlap = False
        hasInvalidTokens = False
        # validate tokens
        while i < len(rawTokens) and not hasOverlap and not hasInvalidTokens:
            if rawTokens[i]["match"].span()[0] - rawTokens[i-1]["match"].span()[1] < 0:
                hasOverlap = True
                raise Exception(
                    'Invalid syntax. "{}" and "{}" are overlaped\nCurrent Tokens: {}'.format(rawTokens[i]["match"][0], rawTokens[i-1]["match"][0], rawTokens))
            elif rawTokens[i]["match"].span()[0] - rawTokens[i-1]["match"].span()[1] > 0:
                hasInvalidTokens = True
                raise Exception(
                    'Invalid syntax. "{}" is invalid\nCurrent Tokens: {}'.format(inputString[rawTokens[i-1]["match"].span()[1]:rawTokens[i]["match"].span()[0]], rawTokens))
            i += 1
        # create list of token nodes
        tokens: list[Node] = []
        for i, t in enumerate(rawTokens):
            # get node type of token
            ntypes = []
            current = t["ttype"]
            before = rawTokens[i-1]["ttype"] if i > 0 else None
            after = rawTokens[i+1]["ttype"] if i < len(rawTokens)-1 else None
            # get potential node types
            for ntype in nodeMappings:
                if nodeMappings[ntype]["isType"](current, before, after):
                    ntypes.append(ntype)

            # check if token node type is valid
            if len(ntypes) > 1:
                raise Exception('Token {} matches node types {}\nCurrent Token: "{}", Previous Token: "{}", Next Token: "{}", i: {}\nRaw Tokens: {}'.format(
                    t["match"][0], ntypes, current, before, after, i, [{"ttype": t["ttype"], "string": t["match"][0]} for t in rawTokens]))
            if len(ntypes) < 1:
                raise Exception(
                    'Token {} matches no node types\nCurrent Token: "{}", Previous Token: "{}", Next Token: "{}", i: {}\nRaw Tokens: {}'.format(t["match"][0], current, before, after, i, [{"ttype": t["ttype"], "string": t["match"][0]} for t in rawTokens]))
            # convert token into node
            tokens.append(Node(token_type=t["ttype"],
                               span=t["match"].span(),
                               node_type=ntypes[0],
                               node_class=nodeMappings[ntypes[0]]["nclass"],
                               value=float(
                t["match"][0]) if (t["ttype"] == TokenType.T_NUM) else t["match"][0].capitalize()
            )
            )
        # add terminator node
        tokens.append(
            Node(TokenType.T_END, (len(rawTokens), len(rawTokens)+1), node_type=NodeType.T_END))

        return tokens
