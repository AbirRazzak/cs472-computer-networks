import socket
import threading
import logger
import output

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

    def perform_action(self, command):
        # TODO: Implement every support command here
        pass
