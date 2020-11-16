# HW4

Abir Razzak </br>
CS472 Computer Networks

## Files

`ARazzak_hw4_questions.txt` - Answers to the questions for HW4.

`./server/` - Code for the server with included changes for HW4 and previous code from HW3.

`./client/` - Previous client code from HW2 (no changes made).

`./server/ftpserverd.conf` - Config file needed for the server. Both `port_mode` and `pasv_mode` cannot be 'NO'.

`.server/configreader.py` - New helper module to read attributes in the config file.

## FTPServer Config File Enhancement

### Server Initialization

When initializing a new server thread, the server object will now check the config file to change the `self.allow_port_mode` and `self.allow_pasv_mode` attributes to false if the config file specifies this. If the config file does not specify these to be false, then by default they will be set to true. If both are set to false, then a fatal error occurs and the server shuts down. This is demonstrated by the addition of the following code in the `__init__()` method of the `FTPServer` object in `server.py`:

```python
allow_port_mode = configreader.get_config_attribute('port_mode')
if allow_port_mode is not None:
   if allow_port_mode is 'No':
         self.support_port_mode = False

allow_pasv_mode = configreader.get_config_attribute('pasv_mode')
if allow_pasv_mode is not None:
   if allow_pasv_mode is 'No':
         self.support_pasv_mode = False

if not self.support_port_mode and not self.support_pasv_mode:
   output.display("FATAL ERROR! Cannot disable both port_mode and pasv_mode. Update your config file.")
   sys.exit(1)
```

### How It's Used

`self.allow_port_mode` is used in the `port_action()` and `eprt_action()` methods in the FTPServer object, while `self.allow_pasv_mode` is used in the `pasv_action()` and `epsv_action()` methods. If either of these attributes are set to false, then the FTPServer will return a `502` response back to the client to let the client know that the action performed is not supported on the server. Here is an example of the server turning a `502` response:

```python
if self.support_pasv_mode:
   # do something
else:
   self.send_to_client("502 This server does not support passive mode")
```
