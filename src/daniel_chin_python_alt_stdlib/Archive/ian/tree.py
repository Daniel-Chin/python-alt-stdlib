import os

def displayNode(depth = 0):
    for node in os.listdir():
        if os.path.isfile(node):
            # file
            print('| ' * depth + '-', node)
        else:
            # folder
            print('| ' * depth + '+', node)
            os.chdir(node)
            displayNode(depth + 1)
            os.chdir('..')

if __name__ == '__main__':
    os.chdir('d:/classnote')
    displayNode()
