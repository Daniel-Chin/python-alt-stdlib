from myfile import sysArgvOrInput
from PIL import Image

def main():
    filename = sysArgvOrInput()
    with open(filename, 'rb') as f:
        with Image.open(f) as image:
            scale = float(input('scale='))
            width = round(scale * image.width)
            height = round(scale * image.height)
            print('Wait for it...')
            new = image.resize([width, height])
            print('saving...')
            new.save(filename + '.resized')
            print('done')

main()
