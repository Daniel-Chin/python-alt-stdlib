def f(cmd):
 print(eval(cmd))

def g():
 global f, g
 del f
 del g

# PERFECTION
