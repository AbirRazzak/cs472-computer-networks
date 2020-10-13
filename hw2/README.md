CS472 (Computer Networks) HW2 by Abir Razzak 

# How to run:
Use Python 3+ to run main.py. Follow the command line args as specified in the hw prompt (hostname, logfilename, port(optional)).
Make sure you are connected to the Internet and any required VPN's for the FTP Server.
Example: python3 main.py 10.246.251.93 mylog.txt

# Sample Log File:
See the sample log file in the directory called "samplelog.txt"

# Questions to be Answered and Turned In:
1. Think about the conversation of FTP – how does each side validate the other (on the connection and data ports – think of each separately)? How do they trust that they’re getting a connection from the right person?

A) They validate every time there is a transaction of data back and forth from each other that the proper ip address is being contacted and through the correct port number. Each side waits for the other to validate each other before proceeding to give or take information from each other.


2. How does your client know that it’s sending the right commands in the right order? How does it know the sender is trustworthy?

A) At first my client will not know if it is sending the correct commands to the FTP Server. It isn't until the Server sends an error message back to the client that the client will then know that a specific command is being requested from the it and will then display to the user what the server expects from them. I suppose the client doesn't also know whether or not where they are connected to is trustworthy. I have not baked in any validation to the client. The client will simply look up the hostname and find it's IP Address and then attempt to connect to it using the specified port number.

# Additional Notes:
There currently a bug in the way that the HELP command works with the given test IP Address 10.246.251.93. No matter how many times I tried, looking up a specific command with the HELP command does not seem to work. For example, sending "HELP PWD" returns the same exact response as just sending "HELP". I haven't figured out why this is the case, so I left a note in the source code that this might occur.
