# Abir Razzak CS472 - HW3 Computer Networks

## How to run

Use 
```py main.py log.txt 2121```
to run the server, with a log file named `log.txt` on the localhost port `2121`.

## Noteworthy Files

- `main.py` - Starting point of the program
- `server.py` - Bulk of where the logic in the program comes from

## Technical Explanations

### main.py

I got the code to make an infinite loop in python from this stackoverflow question here:
https://stackoverflow.com/questions/13180941/how-to-kill-a-while-loop-with-a-keystroke

#### Exit Codes

- 0 - Code ran and exited successfully
- 1 - Error in Command Line Arguments

### authentication.py

The prompt said to save the usernames and passwords in a file, so I decided to save them in a dictionary in a python file.
This python module will store example username and passwords that the FTP server will use as a dictionary.
The module will lookup usernames and match the passwords together.
None of this is encrypted because I think that's overkill for this assignment.
In an actual setting, all of this should be encrypted with hashes and proper storage in a secure format.

### logger.py

The main chunk of code of the logger comes from the logger class in homework 2.


## Resources

Some external resources I used while working on this assignment:

- [Intro to Multi-threading in Python](https://www.tutorialspoint.com/python3/python_multithreading.htm)