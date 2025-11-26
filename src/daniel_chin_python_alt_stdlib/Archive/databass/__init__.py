ENDIAN = 'big'
PARAMS = 'params.json'
HASHMAP = 'hashmap'
CELLS = 'cells'
EXCLUSION = 'exclusion'
HOLE = 1
KEY = 2
LONG_KEY = 3
VALUE = 4

from __future__ import annotations
from os import path
import pickle
from math import log2
from threading import Lock
import json

class DataBass:
    def __init__(
        self, path_to_db, create_new = False, 
        n_hashes = 243, cell_size = 256, n_cells = 729, 
        load_factor = .75, 
    ) -> None:
        self.params_fn    = path.join(path_to_db, PARAMS)
        self.hashmap_fn   = path.join(path_to_db, HASHMAP)
        self.cells_fn     = path.join(path_to_db, CELLS)
        self.exclusion_fn = path.join(path_to_db, EXCLUSION)
        if not (
            path.isfile(self.params_fn) and 
            path.isfile(self.hashmap_fn) and 
            path.isfile(self.cells_fn)
        ):
            if create_new:
                self.createNew(
                    n_hashes, cell_size, n_cells, load_factor, 
                )
            else:
                raise FileNotFoundError(
                    f'"{path_to_db}" doesn\'t contain a DataBass.', 
                )
        
        self.opened = False
        self.lock = Lock()

        self.load_factor = None
        self.n_hashes = None
        self.cell_size = None
        self.n_cells = None
        self.cell_addr_len = None

        self.hashmap = None
        self.cells   = None
    
    def __enter__(self):
        with self.lock:
            # if self.opened:
            #     raise Exception(
            #         'Trying to open an already '
            #         'opened Databass.', 
            #     )
            with open(self.exclusion_fn, 'r+b') as f:
                if f.read(1) == b'1':
                    raise Occupied
                else:   # Possible race condition. Too bad. 
                    f.seek(0)
                    f.write(b'1')
                    f.flush()
            self.opened = True
            with open(self.params_fn, 'r', encoding='utf-8') as f:
                for k, v in json.load(f).items():
                    self.__setattr__(k, v)
            self.cell_addr_len = 1 + int(log2(self.n_cells) / 8)
            self.hashmap = open(self.hashmap_fn, 'r+b')
            self.cells   = open(self.cells_fn,   'r+b')
            return self
    
    def __exit__(self, *_):
        with self.lock:
            self.hashmap.close()
            self.cells  .close()
            with open(self.exclusion_fn, 'r+b') as f:
                f.write(b'0')
            self.opened = False
            return False
    
    def assertOpen(self):
        if not self.opened:
            raise Exception(
                'The databass needs to be opened for '
                'this operation. Use e.g. `with myDb:`.'
            )
    
    def __lookupHashmap(self, i):
        self.hashmap.seek(i * self.cell_addr_len)
        return self.hashmap.read(self.cell_addr_len)
    
    def __lookupCells(self, addr):
        cell = Cell(self, addr)
        self.cells.seek(addr * self.cell_size)
        cell.loads(self.cells.read(self.cell_size))
        return cell
    
    def __decodeKeyCell(self, cell : Cell):
        if cell.type == KEY:
            return cell.key
        elif cell.type == LONG_KEY:
            return pickle.loads(self.__decodeValue(
                cell.long_key_addr, 
            ))

    def __decodeValue(self, addr):
        buffer = []
        while addr != 0:
            cell = self.__lookupCells(addr)
            buffer.append(cell.bytes_value)
            addr = cell.next
        return b''.join(buffer)

    def hash(self, x):
        return hash(x) % self.n_hashes + 1

    def __locate(self, key):
        cell_addr = self.__lookupHashmap(self.hash(key))
        cell_key = None
        e = DbKeyError(f'"{key}" not in databass.')
        if cell_addr == 0:
            e.no_hash = True
            raise e
        while True:
            cell = self.__lookupCells(cell_addr)
            cell_key = self.__decodeKeyCell(cell)
            if cell_key == key:
                break
            if cell.next == 0:
                e.no_hash = False
                e.last_key_cell = cell
                raise e
            cell_addr = cell.next
        return cell
    
    def get(self, key):
        with self.lock:
            self.assertOpen()
            key_cell = self.__locate(key)
            value = self.__decodeValue(key_cell.paired_value_addr)
            return value
    
    def set(self, key, value):
        with self.lock:
            self.assertOpen()
            try:
                key_cell = self.__locate(key)
            except DbKeyError as e:
                ...
            self.__delValueChain(key_cell.paired_value_addr)
            value_addr = self.__dumpValue(value)
            key_cell.paired_value_addr = value_addr
            self.__writeCell(key_cell)
    
    def __delCell(self, addr, last_known_hole = 0):
        hole_addr = last_known_hole
        while hole_addr < addr:
            hole = self.__lookupCells(hole_addr)
            hole_addr = hole.nextHole()
        prev_hole = hole
        next_hole = self.__lookupCells(hole_addr)
        prev_hole.next = addr
        self.__writeCell(prev_hole)
        next_hole.prev = addr
        self.__writeCell(next_hole)
        hole = Cell(self, addr)
        hole.type = HOLE
        hole.next = next_hole.addr
        self.__writeCell(hole)
    
    def __delValueChain(self, addr):
        last_known_hole = 0
        while addr != 0:
            cell = self.__lookupCells(addr)
            self.__delCell(cell.addr, last_known_hole)
            addr = cell.next
            # last_known_hole = cell.addr
            # In fact, addr may not be monotonous for a list. 
    
    def __dumpValue(self, value):
        ...
    
    def __newCell(self):
        root = self.__lookupCells(0)
        hole_addr = root.nextHole()
        hole = self.__lookupCells(hole_addr)
        next_hole_addr = hole.nextHole()
        root.next = next_hole_addr
        self.__writeCell(root)
        return hole_addr
    
    def __writeCell(self, cell : Cell):
        self.cells.seek(cell.addr * self.cell_size)
        cell.dump(self.cells)

class Cell:
    __slot__ = [
        'type', 'next', 'paired_value_addr', 'key', 
        'long_key_addr', 'bytes_value', 
    ]
    def __init__(self, db : DataBass, addr = None) -> None:
        self.db : DataBass = db
        self.cell_addr_len = db.cell_addr_len
        self.addr = addr
    
    def loads(self, data) -> None:
        cell_addr_len = self.cell_addr_len

        bytes_type, data = (
            data[:1 ], 
            data[ 1:], 
        )
        self.type = bytes_type[0]
        bytes_next, data = (
            data[:cell_addr_len ], 
            data[ cell_addr_len:], 
        )
        self.next = int.from_bytes(bytes_next, ENDIAN)
        if self.type == HOLE:
            pass
        elif self.type in (KEY, LONG_KEY):
            bytes_val_addr, data = (
                data[:cell_addr_len ], 
                data[ cell_addr_len:], 
            )
            self.paired_value_addr = int.from_bytes(
                bytes_val_addr, ENDIAN, 
            )
            if self.type == KEY:
                self.key = pickle.loads(data)
            elif self.type == LONG_KEY:
                self.long_key_addr = int.from_bytes(
                    data[:cell_addr_len], ENDIAN, 
                )
        elif self.type == VALUE:
            self.bytes_value = data
    
    def dump(self, f):
        cell_addr_len = self.cell_addr_len

        f.write(bytes([self.type]))
        f.write(self.next.to_bytes(self.cell_addr_len, ENDIAN))
        if self.type == HOLE:
            pass
        elif self.type in (KEY, LONG_KEY):
            f.write(self.paired_value_addr.to_bytes(
                cell_addr_len, ENDIAN, 
            ))
            if self.type == KEY:
                pickle.dump(self.key, f)
            elif self.type == LONG_KEY:
                f.write(self.long_key_addr.to_bytes(
                    cell_addr_len, ENDIAN, 
                ))
        elif self.type == VALUE:
            f.write(self.bytes_value)
    
    def nextHole(self):
        assert self.type == HOLE
        if self.next == 0:
            return self.addr + 1
        else:
            return self.next


class Occupied(Exception):
    '''
    Databass is occupied, maybe by another process. 
    '''

class DbKeyError(KeyError):
    def __init__(self, *arg, **kw):
        super().__init__(*arg, **kw)
        self.has_hash = None
        self.last_key_cell = None
