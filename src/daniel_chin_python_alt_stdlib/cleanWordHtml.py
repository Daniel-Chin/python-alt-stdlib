'''
Input: MS Word generated html file.  
What it does: change encoding to utf-8, remove style info specific to Microsoft Outlook, replace curly double quotes (“) with straights (").  
'''

from tempfile import TemporaryFile
from os import path
import shutil
from myfile import sysArgvOrInput

MSO_9_START = '<!--[if '
MSO_9_END = '<![endif]-->'

def main():
    filename = sysArgvOrInput()
    with TemporaryFile() as tmp:
        with open(filename, 'r', encoding='gb18030') as f:
            during_mso_9 = False
            remains = ''
            try:
                while True:
                    if remains:
                        line = remains
                        remains = ''
                    else:
                        line = next(f)
                    if during_mso_9:
                        parts = line.split(MSO_9_END, 1)
                        if len(parts) == 2:
                            line, remains = parts
                            during_mso_9 = False
                        continue
                    else:
                        parts = line.split(MSO_9_START, 1)
                        if len(parts) == 2:
                            line, remains = parts
                            during_mso_9 = True
                    if MSO_9_START in line or MSO_9_END in line:
                        print(line)
                        raise Exception('Error q3490626')
                    line = line.replace('gb2312', 'utf-8')
                    line = line.replace('“', '&quot;')
                    line = line.replace('”', '&quot;')
                    tmp.write(line.encode('utf-8'))
            except StopIteration:
                pass
        tmp.seek(0)
        with open(filename, 'wb') as f:
            shutil.copyfileobj(tmp, f)
    print('Done. ')

if __name__ == '__main__':
    main()
