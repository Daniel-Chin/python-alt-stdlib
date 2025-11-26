__all__ = ['ImprobableChar', 'guess', 'shift', 'unshift', 
    'RIGHT_BORDER', 'ALL_CHARS', 'RIGHT_BORDER_MAP']

from string import ascii_letters, ascii_lowercase, ascii_uppercase
from functools import lru_cache

class ImprobableChar(Exception):
    pass

keyboard = (
    'qwertyuiop[]', 
    "asdfghjkl;'", 
    'zxcvbnm,./', 
)

@lru_cache(maxsize = sum([len(x) for x in keyboard]) * 2)
def guess(char):
    if char in UNSHIFT_MAP.keys() or char in ascii_uppercase:
        is_shift = True
        char = unshift(char)
    elif char in UNSHIFT_MAP.values() or char in ascii_lowercase:
        is_shift = False
    result = [[]]
    for line in keyboard:
        pos = line.find(char)
        if pos != -1:
            for score in (0, 1, 2):
                for offset in {-score, score}:
                    try:
                        nearby = line[pos + offset]
                        if nearby in ascii_letters:
                            if is_shift:
                                nearby = shift(nearby)
                            result[-1].append(nearby)
                    except IndexError: 
                        pass
                result.append([])
            return result[:-1]
    raise ImprobableChar

UNSHIFT_MAP = {
    '{': '[', 
    '}': ']', 
    '|': '\\', 
    ':': ';', 
    '"': "'", 
    '<': ',', 
    '>': '.', 
    '?': '/', 
}
def unshift(char):
    if char in ascii_letters:
        return char.lower()
    else:
        try:
            return UNSHIFT_MAP[char]
        except KeyError:
            return char

SHIFT_MAP = {v: k for k, v in UNSHIFT_MAP.items()}
def shift(char):
    if char in ascii_letters:
        return char.upper()
    else:
        try:
            return SHIFT_MAP[char]
        except KeyError:
            return char

RIGHT_BORDER_MAP = {
    'p': '[', 
    'l': ';', 
    'm': ',', 
    'P': '{', 
    'L': ':', 
    'M': '<', 
    '[': '[', 
    ';': ';', 
    ',': ',', 
    '{': '{', 
    ':': ':', 
    '<': '<', 
}
RIGHT_BORDER = {*RIGHT_BORDER_MAP}
ALL_CHARS = {*ascii_letters, *RIGHT_BORDER}

if __name__ == '__main__':
    from console import console
    console(globals())
