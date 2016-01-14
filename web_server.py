#author:Anurag Menon
#identity key:anme4174

import configparser
import os
import re
import socket
import select

def Main():
    
    host='localhost'                                           
    config=configparser.ConfigParser(delimiters=(' '))          #Initializing configParser object to read the config file
    config.read('D:\Python\DataCommunication\ws.conf')          #Path of the config file 
    port=int(config.get('port','Listen'))
    root=config.get('root','DocumentRoot')
    defPage=config.get('defaultPage','DirectoryIndex')          #Reading different values from config file
    defList=defPage.split()
    content1=config.items('content')                            
    dic={}
    for temp in content1:
        dic[temp[0]]=temp[1]                                    #Adding the content types supported from the config file
        

    size =1024
    backlog=5
    serv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)       #Creating the socket
    
    serv.bind((host,port))                                       #Binding the socket to the port
    serv.listen(backlog)
    socks=[serv]
    
    while True:
        readable,writable,exceptionavailable= select.select(socks,[],[],10)             #Implementing the select module for multiple requests
        for s in readable:
            if(s==serv):
                client,address=serv.accept()                                         #Accepting the request from client
                socks.append(client)
            else:
                try:
                #client, address = serv.accept()
                    data = s.recv(size)                                              #Receive the request from client                          
                    
                    if data:                                                          #Only process the request if it is a Get request
                        temp=data.decode('utf8')         
                        
                    
                        
                        req=re.match(r'GET.*',temp)                                   #Reg-ex to get the request method and path
                        
                        if hasattr(req,'group'):
                           
                            lis_pt=str(req.group(0)).split(' ')                        
                            path_new=str(lis_pt[1])                                    #Get the path from the regex match
                            vers=str(lis_pt[2])                               
                            vers=vers.strip();
                            if(vers=='HTTP/1.1'):                                      #Check the version type
                                if(re.match("^[a-zA-Z0-9_/.]*$",path_new)):            #Check for special characters in the URI
                                    
                                    if(path_new in defList or path_new=='/'):           #If loop for default path
                                        os.chdir(root)                                  #Change current working directory to root from config file
                                        
                                        fl=open('index.html')                
                                        header=("HTTP/1.1 200 OK\r\n"    
                                                "Connection: Keep-Alive\r\n (or Connection: close)"
                                                "Content-Type:text/html;charset=ISO-8859-1\r\n"
                                                "\r\n")                                                  #The request header
                    
                                        s.sendall(header.encode('utf8'))
                                        output_data=fl.readlines()                                       
                                        for i in range(0,len(output_data)):
                                            s.sendall(output_data[i].encode('utf8'))                #Read the index.html and send the data to the client
                                        
                                    else:                                                      #Else loop to cater request other than default path
                                        file_name,file_extension=os.path.splitext(path_new)
                                        head,tail=os.path.split(path_new)
                                        
                                        content_type=dic.get(file_extension)                    #Check for content type with the ones in config file 
                                        
                                        w=os.path.dirname(os.path.realpath(root+path_new))      
                                        
                                        
                                        bool=os.path.isdir(w)
                                        
                                        if (os.path.isfile(root+path_new) and bool):              #Check if the file or the directory path from the URI exists
                                            os.chdir(w)                                            #Change the working directory to the one given in the path 
                                                                                    
                                    
                                            if file_extension in dic.keys():
                                                
                                                emp_str=" "
                                                fl=open(tail,'rb') 
                                                output=fl.read()
                                                con_len=str(len(output))
                                                header=("HTTP/1.1 200 OK\r\n"
                                                        "Content-Length:"+con_len+"\r\n"
                                                        "Connection: Keep-Alive\r\n (or Connection: close)\r\n"
                                                        "Content-Type:"+content_type+";charset=ISO-8859-1\r\n"
                                                        "\r\n")                                                 #Header for all the other request other than default
                                                
                                                s.send(header.encode('utf8'))
                                                fl=open(tail,'rb') 
                                                output=fl.read()
                                                s.send(output)                                                  #Read the file requested and send the data in binary
                                            else:
                                            
                                                header=("HTTP/1.1 501 Not implemented\r\n"
                                                        "Connection: Keep-Alive\r\n (or Connection: close)\r\n"
                                                        "\r\n")                                                   #Send error for extension not supported by the server
                                            
                                                s.send(header.encode('utf8'))
                                            
                                                s.send(("This content mime type requested is not supported:"+file_extension).encode('utf8'))
                                                          
                                        else:
                                            
                                        
                                            header=("HTTP/1.1 404 Not found\r\n"
                                                    "Connection: Keep-Alive\r\n (or Connection: close)\r\n"
                                                    "\r\n") 
                                        
                                                             
                                            s.send(header.encode('utf8'))                                                 #Send error if file or directory is not found
                                            s.send(("Error 404 File not found:"+path_new).encode('utf8'))
                                else:
                                    
                                    header=("HTTP/1.1 400 Bad Request: Invalid URI\r\n"
                                            "Connection: Keep-Alive\r\n (or Connection: close)\r\n"
                                            "\r\n")
                            
                                    s.send(header.encode('utf8'))                                                        #Send error if the URI is invalid
                                    s.send(("Eror 400 Bad request: Invalid URI:"+vers).encode('utf8'))
                                       
                            else:
                                
                                header=("HTTP/1.1 400 Bad Request: Invalid HTTP Version\r\n"
                                        "Connection: Keep-Alive\r\n (or Connection: close)\r\n"
                                        "\r\n")                                                                          #Send error if HTTP version is other than 1.1
                            
                                s.send(header.encode('utf8'))
                                s.send(("Eror 400 Bad request: Invalid HTTP request:"+vers).encode('utf8'))
                                
                        else:
                            
                            header=("HTTP/1.1 400 Bad Request: Invalid Method\r\n"
                                    "Connection: Keep-Alive\r\n (or Connection: close)\r\n"
                                    "\r\n")                                                                             #Send error if the request is not a GET request
                            
                            s.send(header.encode('utf8'))
                            s.send("Eror 400 Bad request: Not a GET request".encode('utf8'))
                               
                    #client.close()
                except:
                    
                    header=("HTTP/1.1 500 Internal Server Error: Cannot allocate Memory\r\n"
                            "Connection: Keep-Alive\r\n (or Connection: close)\r\n"
                            "\r\n")
                            
                    s.send(header.encode('utf8'))                                                                     #Send the error for any other exception
                    s.send("Eror 500 Internal server error: Cannot allocate memory".encode('utf8'))
                else:
                    s.close()                                                                                      #Close the sockets
                    socks.remove(s)
                

        

if __name__=="__main__":
    Main()