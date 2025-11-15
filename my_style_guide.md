# My Style Guide
This is how I write Python code.  

Later bullet points take precedence:  
- [PEP 8](https://peps.python.org/pep-0008/). 
  - Notably, use the trailing commas in multi-line entries including function args (both def and call).  
- Write what meta-programming would have produced. 
- Vertical alignment is desirable. 
- Comments don't have to be complete sentences. Shorter comments improve readability. 
- Comments can be in Chinese if they correspond to another document in Chinese, e.g. a paper. 
- Avoid abbreviations in names, unless they are well established. Long variable names usually don't affect readability, or even typability. 

## Vertical alignment
````python
x.source_addr[i    ] = 8
x.  dest_addr[i + 1] = 9
````

## Meta-programming
The easiest way to meta-program is to treat code segments as repeating chunks. 

### Example 1
Write single-element tuple as `(1, )`. This way, it generalizes to two-element tuple: `(1, 2, )`. 

### Example 2
Leave a trailing whitespace after the trailing comma:
````python
for a, b, c in zip(
    node_pair, newLink(), reversed(node_pair), 
):
````
This way, adding an element is simply appending a code segment. 

### Example 3
Trailing whitespace in string literals.  
`'I have a dream. '`

## Undecided
Should I use `file=f` or `file = f` for optional arguments? 
