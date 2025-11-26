print('loading...')
from myfile import sysArgvOrInput
import webbrowser
import os

TEMP = 'Python Flash Player.html'

def main():
    os.chdir(os.path.dirname(__file__))
    with open('page.html', 'rb') as f:
        template = f.read()
    swf = sysArgvOrInput().encode()
    page = template.replace(b'__swf__', swf)
    with open(TEMP, 'wb+') as f:
        f.write(page)
    webbrowser.open(TEMP)
    print('A browser window is opened. ')
