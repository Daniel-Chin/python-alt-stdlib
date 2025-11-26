'''
Indent log output in a logical way.  
Try this:  
```python
from indentprinter import indentPrinter
bois = ['Collie', 'Husky', 'Shoob', 'Shibe']
print('All bois:')
with indentPrinter as print:
    [print(x) for x in bois]
```
'''
__all__ = ['indentPrinter', 'IndentPrinter']

class IndentPrinter:
    def __init__(self, saved_print, indent_str = '    '):
        self.depth = 0
        self.saved_print = saved_print
        self.new_line = True
        self.indent_str = indent_str
    
    def __enter__(self):
        self.depth += 1
        return self.print
    
    def __exit__(self, a, b, c):
        self.depth -= 1
    
    def print(self, *args, **kw):
        if self.new_line:
            self.saved_print(self.indent_str * self.depth, end = '')
        self.saved_print(*args, **kw)
        self.new_line = {'end': '\n', **kw}['end'].endswith('\n')

indentPrinter = IndentPrinter(print)
