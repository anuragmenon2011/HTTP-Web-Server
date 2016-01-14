
Code description of the web server:

ws.conf file:

We are reading the server parameters from ws.conf file.The parameters we are reading are port number, the root directory path, the content types supported by the 
server and the default path that needs to be displayed in case of default URI path. The conf file is divided into different sections. We extract the components 
mentioned above using the configparser object. We have hard coded the path of ws.conf in our code (web_server.py).We need to change the path of ws.conf file when we 
change the location of ws.conf file.

Path of config path in the server code: C:/Users/Home/Desktop/DataComm1/www



web_server.py:

We will first extract all the contents of ws.conf file and store it in variables. Then we create the socket using socket.socket method of socket utility.The socket
family would be AF.INET and socket type SOCK_STREAM.We will bind the socket to port number mentioned in ws.conf file and the host would be localhost or '127.0.0.1'.
We would run an always true loop to listen to request from client.We implement the select() module to cater to multiple requests.We then receive the request from client 
using the client.recv() method. if there is a request we would go ahead and process it. In ojur web server we will cater to only GET request. We use regex to check if 
there is GET request in our header. Then we check if the HTTP version is 'HTTP 1.1'. Next would be to check valid URI by checking for special characters in our URI.



We will serve requests in two parts. One part would cater requests for default path and the other part would cater requests if there is a valid path in the URL.Our web
should display the index.html file in case we have a default path. First we change the current working directory to the root directory from config file.Once we change
the directory we will open the file and send it back to the client by utf-8 encoding it with proper response headers. 

If we have a valid path in the URI we will take the directory path and change our working directory to it and the open the file using open() and send it to the client
with proper content type and content length. 



Error Handling:


We will be handling different errors as a part of our web_server code. Firsty we will be checking the 3 error 400: Bad request errors. First for the request method.
(Only GET method should be catered).Then we would be checking for the HTTP version error(Only HTTP 1.1 should be served).The next bad request error would be Bad URI 
exception if there are special characters in our URI.

We will also be throwing error 404 if the file we try to open is not found in the directory path or the directory path is not valid. If the content type or extension 
of the file is not catered by ir web server , it will throw error 501:Not implementd error. ALl the other types of error will be covered under error 500:Internal 
server error.
