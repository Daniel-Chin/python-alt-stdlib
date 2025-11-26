import platform

ESC = b'\x1b\x1b'
CTRL_C = b'\x03'    
# On Linux, stdin.read does not actually give ^C, but raises KeyboardInterrupt
if platform.system().lower() == 'windows':
    WIN_Z_LINUX_D = b'\x1a'
    BACKSPACE = b'\x08'
    DEL = b'\xe0S'
    UP = b'\xe0H'
    DOWN = b'\xe0P'
    LEFT = b'\xe0K'
    RIGHT = b'\xe0M'
    HOME = b'\xe0G'
    END = b'\xe0O'
    CTRL_LEFT = b'\xe0s'
    CTRL_RIGHT = b'\xe0t'
    CTRL_BACKSPACE = b'\x7f'
    CTRL_DELETE =  b'\xe0\x93'
else:
    WIN_Z_LINUX_D = b'\x04'
    BACKSPACE = b'\x7f'
    DEL = b'\x1b[3~'
    UP = b'\x1b[A'
    DOWN = b'\x1b[B'
    LEFT = b'\x1b[D'
    RIGHT = b'\x1b[C'
    HOME = b'\x1b[H'
    END = b'\x1b[F'
    CTRL_LEFT = b'\x1b[1;5D'
    CTRL_RIGHT = b'\x1b[1;5C'
    CTRL_BACKSPACE = b'DOES NOT SUPPORT'
    CTRL_DELETE =  b'\x1b[3;5~'

INVALIDS = set(range(1, 27))
INVALIDS.update({0, 27, 224})
INVALIDS.remove(18) # Ctrl + R
if platform.system().lower() == 'windows':
    INVALIDS.remove(26) # Ctrl + Z
else:
    INVALIDS.remove(4)  # Ctrl + D
def isInvalidToInputChin(op):
    return op[0] in INVALIDS
