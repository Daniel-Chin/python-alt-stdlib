def revDBLL(head):
    cursor = head
    while cursor is not None:
        cursor.prev, cursor.next = cursor.next, cursor.prev
        cursor = cursor.prev
    return cursor.next

def revLL(head):
    cursor = head
    last = None
    while cursor is not None:
        future = cursor.next
        cursor.next = last
        last = cursor
        cursor = future
    return last
