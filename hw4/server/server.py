import socket
import threading
import logger
import output
import authentication
import os
import configreader
import sys

__TIMEOUT__ = 1.0
__LOGIN_LIMIT__ = 5


class FTPServer(threading.Thread):
    def __init__(self, client: socket.socket, address, log: logger.Logger):
        """
        Creates a new thread to handle operations for the FTP Server.
        :param client: Socket connecting the server to the client application
        :param address: IP Address of the client that is connecting to the server
        :param log: Logger object in charge of reading and writing to a log file
        """
        super(FTPServer, self).__init__()
        self.client = client
        self.client.settimeout(__TIMEOUT__)
        self.address = address
        self.logger = log
        self.keep_connection = True
        self.user = None
        self.current_directory = os.getcwd()
        self.pasv = False
        self.epsv = False
        self.port = 20  # default value
        self.netprt = None
        self.netaddr = None
        self.support_port_mode = True
        self.support_pasv_mode = True
        self.failed_login_counter = 0

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

    def send_to_client(self, msg):
        """
        Helper function. Used to send a message to the client application and will log the message sent.
        :param msg: Message to send to the client application
        """
        msg += "\r\n"
        self.client.sendall(msg.encode('utf-8'))
        log_message = "Sent to client at {0}: {1}".format(self.address, msg)
        self.output_and_log(log_message)

    def output_and_log(self, msg):
        self.logger.log(msg)
        output.display(msg)

    def run(self):
        # Let the client know that they have connected.
        self.connected()
        # TODO: Read messages from client
        while self.keep_connection:
            try:
                client_messages = self.get_client_message()
                for client_message in client_messages:
                    self.output_and_log("Received from client at {0}: {1}".format(self.address, client_message))
                    self.perform_action(client_message)
            except socket.error as ex:
                self.output_and_log("Socket Error: Lost connection to client at {0}".format(self.address))
                self.keep_connection = False
        # TODO: Perform action according to message received from client
        # TODO: Send message back after performing action

    def connected(self):
        """
        Sends code 220 to the client application
        """
        command = "220 Connected to FTP server."
        self.send_to_client(command)

    def get_client_message(self):
        """
        Returns messages received from the client application
        :return: All current messages received from the client application
        """
        response = []
        while True:
            try:
                data = self.client.recv(1024)
                response.append(data.decode("utf-8").replace("\r\n", ""))
            except socket.timeout:
                break
        return response

    def perform_action(self, full_command):
        command_split = full_command.split()
        command = command_split[0]
        # TODO: Implement every support command here
        if command.upper() == "USER":
            self.user_action(command_split[1])
        if command.upper() == "PASS":
            self.pass_action(command_split[1])
        if command.upper() == "QUIT":
            self.quit_action()
        if command.upper() == "PWD":
            self.pwd_action()
        if command.upper() == "CWD":
            self.cwd_action(command_split[1])
        if command.upper() == "LIST":
            self.list_action()
        if command.upper() == "PASV":
            self.pasv_action()
        if command.upper() == "EPSV":
            self.epsv_action()
        if command.upper() == "PORT":
            self.port_action(command_split[1])
        if command.upper() == "EPRT":
            eprt_split = full_command.split("|")
            self.eprt_action(eprt_split[1], eprt_split[2], eprt_split[3])
        if command.upper() == "RETR":
            self.retr_action(command_split[1])
        if command.upper() == "STOR":
            self.stor_action(command_split[1])
        if command.upper() == "CDUP":
            self.cdup_action()

    def user_action(self, user):
        """
        Handles the USER command from the client application
        :param user: Username to login to the server with
        """
        self.user = user
        self.output_and_log("Set user for {0} to {1}".format(self.address, user))
        self.send_to_client("331 Please specify the password.")

    def pass_action(self, password):
        """
        Handles the PASS command from the client application
        :param password: Password to login to the server with
        """
        # Must provide USER before entering PASS
        if not self.user:
            self.send_to_client("530 Provide USER before PASS.")
        else:
            if authentication.auth_user(self.user, password):
                self.send_to_client("230 Login successful")
                self.failed_login_counter = 0
            else:
                self.send_to_client("530 Authentication Failed")
                self.failed_login_counter += 1
                if self.failed_login_counter == __LOGIN_LIMIT__:
                    self.send_to_client("530 Login Failed too many times, exiting connection")
                    self.quit_action()

    def quit_action(self):
        """
        Handles the QUIT command from the client application
        """
        self.keep_connection = False
        self.send_to_client("221 Quitting FTP Server Connection")
        self.client.shutdown(socket.SHUT_WR)

    def pwd_action(self):
        """
        Handles the PWD command from the client application
        """
        self.send_to_client("257 {0}".format(self.current_directory))

    def cwd_action(self, path):
        """
        Handles the CWD command from the client application
        :param path: Path to change current working directory
        """
        # Check that given path is valid
        if os.path.isdir(path):
            # Change directory to the path
            os.chdir(path)
            # Sanitize the path and set the current directory to it
            self.current_directory = os.path.normpath(path)
            self.send_to_client("250 Current working directory changed to {0}".format(path))
        else:
            self.send_to_client("550 Invalid directory given")

    def list_action(self):
        """
        Handles the LIST command from the client application
        """
        ls = os.listdir(self.current_directory)
        self.send_to_client("150 Sending file data")
        for file in ls:
            self.send_to_client(file)

    def pasv_action(self):
        """
        Handles the PASV command from the client application
        """
        if self.support_pasv_mode:
            self.pasv = True
            self.send_to_client("227 Entering passive mode")
        else:
            self.send_to_client("502 This server does not support passive mode")

    def epsv_action(self):
        """
        Handles the EPSV command from the client application
        """
        if self.support_pasv_mode:
            self.epsv = True
            self.send_to_client("229 Entering extended passive mode")
        else:
            self.send_to_client("502 This server does not support extended passive mode")

    def port_action(self, port):
        """
        Handles the PORT command from the client application
        :param port: Port number to change to
        """
        if self.support_port_mode:
            try:
                if int(port) < 0 or int(port) > 65535:
                    self.send_to_client("522 Port out of range.")
                else:
                    self.port = port
                    self.pasv = False
                    self.send_to_client("200 Valid port given")
            except ValueError as ex:
                self.output_and_log("PORT error with {0}: {1}".format(self.address, ex))
                self.send_to_client("500 Invalid port number given")
        else:
            self.send_to_client("502 This server does not support port mode")

    def eprt_action(self, netprt, netaddr, tcpport):
        """
        Handles the EPRT command from the client application
        :param netport: Network protocol of extended address
        :param netaddr: Network address of extended address
        :param tcpport: Transport address of extended address
        :return:
        """
        if self.support_port_mode:
            try:
                if int(netprt) == 1 or int(netprt) == 2:
                    self.netprt = netprt
                    self.netaddr = netaddr
                    self.port = tcpport
                    self.pasv = False
                    self.send_to_client("200 Valid port given")
                else:
                    self.send_to_client("522 Server does not support requested network protocol")
            except ValueError as ex:
                self.output_and_log("EPRT error with {0}: {1}".format(self.address, ex))
                self.send_to_client("500 Invalid port number given")
        else:
            self.send_to_client("502 This server does not support extended port mode")

    def retr_action(self, path):
        """
        Handles the RETR command from the client application
        :param path: Filepath in the server to retrieve file
        """
        try:
            file = open(path, 'r')
            file_contents = file.read()
            self.send_to_client("150 File okay, sending file contents")
            self.send_to_client(file_contents)
        except IOError as ex:
            self.output_and_log("RETR error with {0}: {1}".format(self.address, ex))
            self.send_to_client("550 File does not exist")

    def stor_action(self, path):
        """
        Handles the STOR command from the client application
        :param path: Filepath in the server to store file
        """
        try:
            pass
            file = open(path, 'w+')
            self.send_to_client("150 File okay, start writing file contents")
            content = str(self.client.recv(1024))
            file.write(content)
            file.close()
            self.send_to_client("150 File okay, finished writing")
        except IOError as ex:
            self.output_and_log("STOR error with {0}: {1}".format(self.address, ex))
            self.send_to_client("550 File does not exist")

    def cdup_action(self):
        """
        Handles the CDUP command from the client application
        """
        # Code found at https://www.kite.com/python/answers/how-to-go-up-one-directory-in-python
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        self.current_directory = os.getcwd()
        self.send_to_client("250 Changed directory up")
