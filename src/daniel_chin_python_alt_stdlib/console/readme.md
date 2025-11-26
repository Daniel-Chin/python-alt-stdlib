Runtime embedded interactive python shell, just like IPython.  

Windows only. If not windows, `console()` calls `IPython.embed()`.  
Usage: `console(globals())` or `console({**locals(), **globals()})`  

Advantages over IPython:  
* Lighter. Launches very quickly.  
* Other threads can still print things when user is inputting commands  
* Tab auto-completes your phrase, even under Windows! (I'm proud.)  
* Tired of having to `import` to test your module everytime you make an edit? `restart()` is what you need here. Ctrl+R does the same!  

Issues:  
* Reassigning module global variables will not be visible to module native codes. Sorry.  
* For unknown reasons, you cannot declare any name present in kernal.py that is invisible to the env.  
* Sometimes inline generator cannot access namespace. I can't stably replicate this issue, and I don't know what this is about.  

Fixed Issues:  
* If you wanna scroll up, you don't need to input() anymore!  
* Multi-line code continuation is implemented!  
* If input command is longer than terminal width, camera rolls.  

Future:  
* Consider adding a dynamic `return` feature.  
* Study passing namespace into `exec` and `evel` and use them.  
