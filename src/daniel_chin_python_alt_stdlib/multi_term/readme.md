Provides multiple terminal windows for output.  
Supports Windows OS.  

For demo, run file `__main__.py` or run this module via `py -m multi_term`.  
In the demo, there are multiple levels of output (info, debug, warning, error), redirected to each terminal.  

Uses sockets for inter-process communication.  
Future work:  
* Support more OSes.  
* Allow input from other terminals.  
* Replace lock for semaphore to launch terminals in parallel.  
* Remote terminal?  
