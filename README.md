# CS480-HW2

## Requirements
python 3.8

## Credits
- modified from https://github.com/gnebehay/parser
- AST node tree print modified from https://stackoverflow.com/questions/20242479/printing-a-tree-data-structure-in-python

## Calculator

```sh
python calc.py <options> <expressions>
```

```<options> ```:&nbsp;&nbsp;start with "--" and add flags right after  

* e&nbsp;&nbsp;evaluate expressions given after the options (max 100 expressions)  
* r&nbsp;&nbsp;start "REPL"  

```<expressions>```:&nbsp;&nbsp;mathematical expression to be evaluated in quotation marks max 100 in a row separated by space, the rest are not evaluated (only used if "e" option flag is given)  

## Testing
```sh
python test.py <input string> <options> <modules>
```

```<input string>```:&nbsp;&nbsp;any arithmatic operation between quotes  

```<options>```:&nbsp;&nbsp;starts with '--' and add flags after
* m&nbsp;&nbsp;Test certain modules ["MathTokenizer", "MathParser", "MathCompute"]
* v&nbsp;&nbsp;Verify results of testcases
* g&nbsp;&nbsp;Create graphviz representation
* i&nbsp;&nbsp;Create images from graphvis (requires graphvis to be installed)
* p&nbsp;&nbsp;Print the contents of each node

```<modules>```:&nbsp;&nbsp;any of ["MathTokenizer", "MathParser", "MathCompute"] maximum 3, (only used if 'm' option flag is used)  