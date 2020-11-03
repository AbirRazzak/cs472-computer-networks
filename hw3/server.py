import socket
import threading
import logger
import output
import authentication

__TIMEOUT__ = 1.0

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
            else:
                self.send_to_client("530 Authentication Failed")

    def quit_action(self):
        """
        Handles the QUIT command from the client application
        """
        self.keep_connection = False
        self.send_to_client("221 Quitting FTP Server Connection")
        self.client.shutdown(socket.SHUT_WR)
