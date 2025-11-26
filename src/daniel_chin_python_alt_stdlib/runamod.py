'''
Run a python module but it waits at the end as if you called it in command line.  
'''
import traceback

def runamod(module):
    try:
        module.main()
    except:
        traceback.print_exc()
    finally:
        input('Press Enter...')
