'''
Prints QR code to terminal. Ascii only: black whitespace and white whitespace
'''
import qrcode
from colorama import Fore, Back, Style, init
init()

def getLines(data):
    lines = []
    qrCode = qrcode.main.QRCode()
    qrCode.add_data(data)
    matrix = qrCode.get_matrix()
    for row in matrix[2:-2]:
        line = []
        for pixel in row[3:-3]:
            if pixel:
                line.append(Back.BLACK)
            else:
                line.append(Back.WHITE)
        line.append('')
        lines.append('  '.join(line))
    return lines

def printQR(data, data_2 = None):
    if data_2 is None:
        lines = getLines(data)
    else:
        lines_1 = getLines(data)
        lines_2 = getLines(data_2)
        delta = len(lines_2) - len(lines_1)
        for i in range(delta):
            lines_1.append(lines_1[-1])
        lines = [x + y for x, y in zip(lines_1, lines_2)]
    print(*lines, Style.RESET_ALL, sep = '\n')

if __name__ == '__main__':
    input('You can print stuff before. Enter...')
    printQR('Test text', 'Other')
    print('And after. ')
    input('Enter...')
