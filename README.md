# crawler
A simple multi-threaded client-server web crawler that can get keywords, emails, and links up to different depths

# Running
The program is written following a server/client architecture. The client provides the server with the links and request of finding links,
keywords locations, or email addresses. The server searches for the keyword, links, or email adresses in all the webpages up to a depth
specified by the client and returns all the instances found. The server uses a breadth-first search algorithm for finidng every instance of 
requested items.

To run, first run the server:
 ```
 python server.py
 ```
 
 and then run the client.
 
```
python client.py
```

# Further Notes
At this time, the implementation is not multithreaded. So a new request cannot be issued before the results of previous request is displayed.
