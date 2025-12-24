'''
A text-to-text render of markdown that handles line breaking.  
Removes all indentation.  
Some string operations are not the most efficient. Readability first.  
'''

def render_markdown_line_breaking(raw: str) -> str:
    lines = raw.strip().splitlines()
    unindent = '\n'.join(line.lstrip() for line in lines)
    return helper_join([
        ('\n\n', '\n\n'), 
        ('  \n', '\n'), 
        ('\n', ' '), 
    ], unindent)

def helper_join(rules: list[tuple[str, str]], raw: str) -> str:
    delimiter, connector = rules[0]
    return connector.join(helper_split(rules[1:], delimiter, raw))

def helper_split(rules: list[tuple[str, str]], delimiter: str, raw: str):
    for part in raw.split(delimiter):
        stripped = part.strip()
        if not stripped:
            continue
        yield helper_join(rules, stripped) if rules else stripped

def test():
    raw = '''
    This is a paragraph with some text that should be wrapped 
    according to the rules specified.  

    Here is a new paragraph that should be separated by two newlines.  
    This another line that is the same paragraph but on a new line.  

    Finally, a space should be added
    when wrapping with \\n without a space.  
    '''
    print('<result>', render_markdown_line_breaking(raw), '</result>', sep='')
    print()
    print(repr(render_markdown_line_breaking(raw)))

if __name__ == '__main__':
    test()
