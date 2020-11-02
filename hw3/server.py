import socket
import threading
import logger


class FTPServer(threading.Thread):
    def __init__(self, client: socket, address, log: logger.Logger):
        """
        Creates a new thread to handle operations for the FTP Server.
        :param client: Socket connecting the server to the client application
        :param address: IP Address of the client that is connecting to the server
        :param log: Logger object in charge of reading and writing to a log file
        """
        super(FTPServer, self).__init__()
        self.client = client
        self.address = address
        self.logger = log

    def send_to_client(self, msg):
        """
        Helper function. Used to send a message to the FTP Server directly.
        :param msg: Message to send to the FTP Server.
        """
        msg += "\r\n"
        self.client.sendall(msg.encode('utf-8'))
        self.logger.log("Sent to client at {0}: {1}".format(self.address, msg))

    def run(self):
        # Let the client know that they have connected.
        self.connected()
        # TODO: Read messages from client
        # TODO: Perform action according to message received from client
        # TODO: Send message back after performing action

    def connected(self):
        """
        Sends code 220 to the client application
        """
        command = "220 Connected to FTP server."
        self.send_to_client(command)
