import os

os.chdir('d:/classnote')
to_do = ['.']

while to_do:
    now_doing = to_do.pop(0)
    children = os.listdir(now_doing)
    for child in children:
        if os.path.isdir(child):
            to_do.append(now_doing + '/' + child)
        print(child)
