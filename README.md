# StressServer
A simple server to simulate cpu stress via a REST API.

The web server will respond to a number of GTTP GET requests which depending on the parameters will simulate stress on the running VM.
While HTTP POST would propably be more suited, the functionality is implemented with GET to make it easier tou se with either cli tools (curl, web browser or applications  (POSTMAN).)

For the PoC developed the web server needs to be able to redirect each accepted request to the nect layer.


                                                                                                                            
+---------+                +----------+                              +----------+                                           
|         |                |          |                              |          |                                           
|   WS1   |--------------->|    WS2   |----------------------------->|   WS_S   |                                           
|         |                |          |              |               |          |                                           
+---------+                +----------+              |               +----------+                                           
                                                     |                                                                      
                                                     |                                                                     
                                                     |                                                                      
                                                     |               +----------+                                           
                                                     |               |          |                                           
                                                     --------------->|  WS_G    |                                           
                                                                     |          |                                           
                                                                     +----------+                                           
                                                                                                                            
REDIRECT:
    To get the targets for the rediret a text file will be used. Atm the filename will be hardcoded (targets.txt)
    The format of the file will be:
    Line 1: A number signifying percentage.
    Line 2: The target to redirect the accepted request. The redirection will be done on the propability of the number of first line. If number is 100 or more all of the requests will be forwarded.
    Line 3: The target to redirect the accepted request. The redirection will be done on the propability of the number of first line (100 -value). In case of multiple targets the value should not be over 100 and will be capped at 90.
    All values can be modified on run time by editing the targets.txt file. If required an API will also be implemented.

REDIRECT RULES:

WS1-->WS2:
    Will usually forward. The target file should have 2 entries. One number and one target. A flag on the request will allow overide of the percentage and either forward every or none request.                                                                
WS2-->WS_S/WS_G:
    Will always forward. The target file should have 3 entries. One number and two targets. IF the number is for example 80, 80% of the requests will be forwarded to the first target (2nd entry of the text file) and 20% will be redirected to the second target (3rd entry).    
WS_S/WS_G-->Final Destination. If exists same rules as WS1->WS2 apply. 

Target.txt examples:
Example1:
    Contents:
        host
    Meaning:
        First/third layer. Will forward all messages (unless overiden by parameters) 
Example2:
    Contents:
        90
    Meaning:
        Not valid 
Example3:
    Contents:
        90
        host
    Meaning:
        First/third layer. Will forward  90% of messages (unless overiden by parameters) 
Example4:
    Contents:
        host1
        host2
    Meaning:
        Second layer. Will forward  90% (default) of messages to host1 and 10% to host 2 
Example5:
    Contents:
        70
        host1
        host2
    Meaning:
        Second layer. Will forward  70% (default) of messages to host1 and 30% to host 2 
Example6:
    Contents:
        host1
        host2
        host3
    Meaning:
        Not valid 
        
