class Node:
    def __init__(self, x):
        self.next = None
        self.value = x
    
    def __repr__(self):
        if self.next is None:
            return repr(self.value)
        else:
            return repr(self.value) + ' -> ' + repr(self.next)
    
    def print(self):
        print(self.value, end = '')
        if self.next is None:
            print()
        else:
            print(' -> ', end = '', flush = True)
            self.next.print()

# Daniel's solution #1
def flipChunks(root, k):    # space = O(1); time = O(N)
    cursor = root       # space = O(1)
    result_root = None  # space = O(1)
    last_chunk_end = None   # space = O(1)
    try:
        while True:     # time = O(N)
            chunk_root, chunk_end, cursor = flipOneChunk(
                cursor, k
            )       # space = O(1); time = O(k)
            chunk_end.next = cursor
            if result_root is None:
                result_root = chunk_root
            else:
                last_chunk_end.next = chunk_root
            last_chunk_end = chunk_end
    except TypeError:
        if result_root is None:
            return root
    return result_root

# helper function for solution #1
def flipOneChunk(root, k):  # # space = O(1); time = O(k)
    left = root     # space = O(1)
    try:
        cursor = left.next      # space = O(1)
        right = cursor.next     # space = O(1)
    except AttributeError:
        return False
    for _ in range(k - 2):  # time = O(k)
        if right is None:
            while cursor is not root:
                right = cursor
                cursor = left
                left = left.next
                cursor.next = right
            return False
        cursor.next = left
        left = cursor
        cursor = right
        right = cursor.next
    cursor.next = left
    return cursor, root, right

# convert list to linked list
def LL(x):
    root = Node(x[0])
    cursor = root
    for i in x[1:]:
        cursor.next = Node(i)
        cursor = cursor.next
    return root

def test(func = flipChunks):        
    for k in range(2, 5):
        print('k =', k)
        for l in range(1, 10):
            func(LL(range(l)), k).print()
        print()

# Daniel's solution, #2
def elegant(root, k):
    chunk_root = Node(None)     # helper head
    chunk_root.next = root
    result_root = chunk_root
    while longerThan(chunk_root, k):
        for i in range(k-1, -1, -1):
            cursor = chunk_root
            for j in range(k):
                if j < i:
                    swap(cursor)
                cursor = cursor.next
        chunk_root = cursor
    return result_root.next

def swap(A):
    # "A -> B -> C -> D" becomes "A -> C -> B -> D"
    B, C, D = A.next, A.next.next, A.next.next.next
    A.next, C.next, B.next = C, B, D

def longerThan(x, l):
    for _ in range(l):
        x = x.next
        if x is None:
            return False
    return True

if __name__ == '__main__':
    # from console import console
    # console({**locals(), **globals()})
    # elegant(LL(range(9)), k = 4).print()
    test(func = elegant)

# first attempt. fail
def badbadbad(root, k):
    right = root
    result_root = None
    while True:
        left = right
        cursor = left.next
        right = cursor.right
        start = left
        for _ in range(k - 2):
            cursor.next = left
            left = cursor
            cursor = right
            right = cursor.right
        if result_root is None:
            result_root = cursor
        cursor.next = left
        start.next = right
    return result_root
