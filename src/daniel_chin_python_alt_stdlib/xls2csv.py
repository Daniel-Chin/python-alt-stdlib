'''
Convert xls or xlsx to csv.  
This loads the entire file content into RAM. Be careful with big files.  
'''

import pandas as pd
from myfile import sysArgvOrInput
from os.path import extsep

def convert(filename):
  content = pd.read_excel(filename).to_csv()
  filename = extsep.join(filename.split(extsep)[:-1]) + extsep + 'csv'
  with open(filename, 'w') as f:
    f.write(content)

def main():
  filename = sysArgvOrInput()
  convert(filename)
  print('ok')

if __name__ == '__main__':
  main()
