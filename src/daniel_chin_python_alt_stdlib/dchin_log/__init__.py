'''
Log script parameters as well as terminal output to files.  
Useful for simulation runs / deep learning experiments.  
'''
from os import path, mkdir
from datetime import datetime
import traceback

class NoSuchParameter(Exception): pass

class Param:
    def __init__(self) -> None:
        object.__setattr__(self, 'records', [])
    
    def __getRecord(self, __name: str):
        for record in self.records:
            if record[0] == __name:
                return record
        raise NoSuchParameter(f'`{__name}`')

    def __getattr__(self, __name: str):
        return self.__getRecord(__name)[1]

    def __setattr__(self, __name: str, __value) -> None:
        try:
            self.__getRecord(__name)[1] = __value
        except NoSuchParameter:
            self.records.append([__name, __value])
    
    def __repr__(self) -> str:
        s = []
        s.append('Param {')
        for n, v in self.records:
            s.append(f'  {n} = {v}')
        s.append('}')
        return '\n'.join(s)

class DChinLog:
    def __init__(self, filename) -> None:
        self.param = Param()
        if filename.lower().endswith('.py'):
            dir_name = path.join(
                path.dirname(__file__), 
                'dchin_log', 
            )
            try:
                mkdir(dir_name)
            except FileExistsError:
                pass
            self.filename = path.join(
                dir_name, 
                datetime.now().strftime('%Y-%m-%d_%H.%M.%S.log'), 
            )
        else:
            self.filename = filename

    def __print(self, *args, **kw):
        print(*args, **kw)
        try:
            print(*args, file=self.f, **kw)
        except AttributeError:
            raise Exception('Cannot print without entering the context.')
    
    def __enter__(self):
        self.f = open(self.filename, 'w', encoding='utf-8')
        print(self.param, file=self.f)
        print(file=self.f)
        return self.__print

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:    # just in case...
            traceback.print_exception(
                exc_type, exc_val, exc_tb, file=self.f, 
            )
        finally:
            self.f.close()
