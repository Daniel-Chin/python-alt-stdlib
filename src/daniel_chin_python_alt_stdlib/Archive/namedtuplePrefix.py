from collections import namedtuple

def namedtuplePrefix(type_name, keys, **kw):
    TheNamedtuple = namedtuple(type_name, keys, **kw)
    class TheNamedtuplePrefix(TheNamedtuple):
        def __init__(self, *a, **kw):
            TheNamedtuple.__init__(self, *a, **kw)
            self.key_i_max = max(
                [keys.index(x) for x in kw.keys()]
                + [len(a)], 
            )
        
        def __repr__(self):
            params = []
            for k, v in self[:self.key_i_max]:
                params.append(f'{k}={v}')
            return f'{type_name}({", ".join(params)})'
    return TheNamedtuplePrefix

if __name__ == '__main__':
    from console import console
    console({**globals(), **locals()})
