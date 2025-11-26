## Cell
````
type = HOLE | KEY | LONG_KEY | VALUE
next
payload
````
`next` links to the next cell.  
- If `next == 0`, 
  - If `type == HOLE`, it means: all cells to the right are empty. 
  - Otherwise, it means: end of list. 

For `HOLE`, the `payload` is `prev`. The `next` is the next hole on the right.  
For `KEY`, the `payload` is `paired_value_addr + key`. The `next` is the next key with the same hash.  
For `LONG_KEY`, the `payload` is `paired_value_addr + long_key_addr`. The `next` is the next key with the same hash.  
For `VALUE`, the `payload` is the value. The `next` is the continuation of value.  
