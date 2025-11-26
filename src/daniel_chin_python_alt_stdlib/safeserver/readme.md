A simple file server.  
Serves file in a folder.  
Has a simple html page interface.  
Built upon safe_http.py. Please see its documentation.  
Problems:  
* Does not sanitize html. But Don't panic! This is a file server and the threat only originates from local file names. Plus, "<>" is not allowed in filename.  
