'''
pip install, and imports
'''
import pip

def pimport(name):
    try:
        return __import__(name)
    except ImportError:
        pip.main(['install', name])
        return __import__(name)
