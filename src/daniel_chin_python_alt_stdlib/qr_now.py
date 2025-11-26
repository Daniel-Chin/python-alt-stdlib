'''
Make a QR code instantly
'''
import qrcode
import sys

if len(sys.argv) >= 2:
    url = sys.argv[1]
else:
    url = input('url = ')

print('making qrcode...')
qrcode.make(url).show()
