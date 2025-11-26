'''
Creates a react component file containing boilerplate code.  
'''

from myfile import sysArgvOrInput
import os

CODE = '''import React from 'react';

const %s = () => {
  return (
    <div>
      
    </div>
  );
};

export default %s;
'''

def create(name):
  with open(name + '.js', 'w', newline='\n') as f:
    f.write(CODE % (name, name))

def main():
  op = sysArgvOrInput('Component name: ')
  names = []
  while op:
    create(op)
    names.append(op)
    op = input('Component name: ')
  folder = os.getcwd().replace('\\', '/').split('/')[-1].strip('/')
  print(*["import %s from '../%s/%s';" % (x, folder, x) for x in names], sep = '\n')

if __name__ == '__main__':
  main()
