import os
from typing import List, Union
from node import Node
node_counter = 1

# -------------------------------------------------------------------------------------
# Credits:
# Based of work from https://github.com/gnebehay/parser

def label(node: Union[Node, List[Node]]):
    global node_counter
    if type(node) is Node:
        node.id = node_counter
        node_counter += 1
        for child in node.children:
            label(child)
    elif type(node) is list:
        for n in node:
            n.id = node_counter
            node_counter += 1
            for child in n.children:
                label(child)


def to_graphviz(node, num=None, testCase=None, png=False):
    dir = 'graphviz'
    if not(os.path.exists(dir) or os.path.isdir(dir)):
        os.mkdir(dir)
    f = open('./'+dir+"/graphviz_input" +
             ("_" + str(num) if num != None else ""), "wt")
    f.write('graph "' + (testCase if testCase != None else '') + '"'+'\n')
    f.write('{'+'\n')

    if type(node) is Node:
        _to_graphviz(node, f)
    elif type(node) is list:
        for n in node:
            _to_graphviz(n, f)

    f.write('}'+'\n')
    f.close()
    if png:
        os.system('dot -Tpng '+dir+"/graphviz_input"+("_" + str(num) if num !=
                  None else "")+' -o '+dir+'/output'+("_" + str(num) if num != None else "")+'.png')


def _to_graphviz(node, f):
    f.write('n{} [label="{}"] ;'.format(node.id, node.value) + '\n')

    for child in node.children:
        f.write('n{} -- n{} ;'.format(node.id, child.id) + '\n')
        _to_graphviz(child, f)
# -------------------------------------------------------------------------------------