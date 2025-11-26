'''
Your code requires Daniel's PythonLib? Use this template to import the required modules.  
'''

try:
    from some_module_foo import bar
except ImportError as e:
    module_name = str(e).split('No module named ', 1)[1].strip().strip('"\'')
    if module_name in (
        'some_module_foo', 
    ):
        print(f'Missing module {module_name}. Please download at')
        print(f'https://github.com/Daniel-Chin/Python_Lib')
        input('Press Enter to quit...')
    raise e
