# CS472 (Computer Networks) HW2 by Abir Razzak 

## How to run:
Use Python 3+ to run main.py. Follow the command line args as specified in the hw prompt (hostname, logfilename, port(optional)).
Make sure you are connected to the Internet and any required VPN's for the FTP Server.
Example: python3 main.py 10.246.251.93 mylog.txt

## Additional Notes:
There currently a bug in the way that the HELP command works with the given test IP Address 10.246.251.93. No matter how many times I tried, looking up a specific command with the HELP command does not seem to work. For example, sending "HELP PWD" returns the same exact response as just sending "HELP". I haven't figured out why this is the case, so I left a note in the source code that this might occur.
