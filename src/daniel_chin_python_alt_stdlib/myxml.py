'''
XML parser
'''
import xml.etree.ElementTree as ET

def display(element, shrink = True, depth = 0):
    if shrink:
        to_display = smartShrink(element.text)
    else:
        to_display = element.text
    print('-'*depth,element.tag,':',to_display)
    for child in element:
        display(child,shrink,depth+1)

def smartShrink(raw):
    if type(raw) is str and len(raw)>30:
        return raw[0:27]+'...'
    else:
        return raw

def readXML(filename):
    s=open(filename,'r').read()
    return ET.fromstring(s)

if __name__=='__main__':
    import sys
    with open(sys.argv[1], 'r') as f:
        root=ET.fromstring(f.read())
    display(root)
    input('Enter...')
