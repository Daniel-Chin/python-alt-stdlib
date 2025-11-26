'''
creality_cr6-se_gcode_postprocess
'''

import os

TAG = '_G28_once'

def main():
    for fn in os.listdir():
        root, ext = os.path.splitext(fn)
        if ext.lower() == ".gcode" and not root.endswith(TAG):
            with open(fn, 'r') as f:
                lines = f.readlines()
            with open(root + TAG + ext, 'w') as f:
                for line in lines:
                    if line.startswith('G28 X0 Y0'):
                        print('Detected G28 X0 Y0')
                        f.write('G28\n')
                    elif line.startswith('G28 Z0'):
                        print('Detected G28 Z0')
                    else:
                        f.write(line)
            print(f"{fn} -> {root + TAG + ext}")

if __name__ == "__main__":
    main()
