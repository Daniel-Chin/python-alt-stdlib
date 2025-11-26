'''
Interactive git commit and push.  
'''
from subprocess import Popen

def main():
    Popen(['uv', 'run', 'python', 'compile_readme.py']).wait()
    Popen(['git', 'add', '-A']).wait()
    Popen(['git', 'status']).wait()
    try:
        message = input('OK? Commit message: ')
        message = message or 'auto commit'
        Popen(['git', 'commit', '-m', message]).wait()
        Popen(['git', 'push']).wait()
        input('Enter...')
    except (EOFError, KeyboardInterrupt):
        print('Did not commit. ')
        from os import system as terminal
        terminal('cmd')
        
main()
