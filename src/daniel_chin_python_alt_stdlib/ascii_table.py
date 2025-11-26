'''
A beautiful script to print the ascii table. 
'''

N_ROW = 20
N_COL = 5
START = 32

rows = [[] for _ in range(N_ROW)]
for i in range(START, START + N_ROW * N_COL):
    rows[0].append('|'.join((format(i, '3'), format(hex(i)[2:], '3'), chr(i))))
    rows.append(rows.pop(0))
[print(' \t'.join(x)) for x in [['DEC|HEX|CHAR'] * N_COL] + rows]
input('Enter to quit...')
