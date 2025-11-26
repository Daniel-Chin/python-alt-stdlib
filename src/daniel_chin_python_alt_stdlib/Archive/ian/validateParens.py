def nani(raw):
    chars = [*raw]
    depth = 0
    for i, char in reversed([*enumerate(chars)]):
        if char == ')':
            depth += 1
        elif char == '(':
            depth -= 1
        if depth < 0:
            chars.pop(i)
            depth = 0
    i = 0
    while depth > 0:
        if chars[i] == ')': 
            chars.pop(i)
            depth -= 1
        else:
            i += 1
    return ''.join(chars)

def test():
    assert nani('lee(t(c)o)de)') == 'lee(t(co)de)'
    assert nani('a)b(c)d') == 'ab(c)d'
    assert nani('))((') == ''
    assert nani('(a(b(c)d)') == 'a(b(c)d)'

test()
