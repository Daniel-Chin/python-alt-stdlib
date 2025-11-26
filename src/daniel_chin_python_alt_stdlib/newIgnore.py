'''
Creates an empty `.gitignore` file.  
This is useful because Windows File Explorer forbids you from naming a file without base name, and `>` now creates files in UTF-16 with BOM encoding.  
'''

with open('.gitignore', 'w', encoding='utf-8') as f:
    f.write('*.pyc\n')
