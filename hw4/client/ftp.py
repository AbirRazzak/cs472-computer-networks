import socket

# Edit to change how long the program waits before returning information
__TIMEOUT__ = 1.0


class FTPConnection:
    # Class FTPConnection - used to handle all commands ftp server commands sent, and responses received
    server_socket = None

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self, ip, port):
        """
        Connects to the FTP Server
        :param ip: IP Address to connect to
        :param port: Port number to connect to
        """
        self.server_socket.connect((ip, int(port)))
        self.server_socket.settimeout(__TIMEOUT__)

    def get_server_response(self):
        """
        Returns the responses from the FTP Server
        :return: All current responses from the FTP Server
        """
        response = []
        while True:
            try:
                data = self.server_socket.recv(1024)
                response.append(data.decode("utf-8").replace("\r\n", ""))
            except socket.timeout:
                break
        return response

    def send_to_server(self, msg):
        """
        Helper function. Used to send a message to the FTP Server directly.
        :param msg: Message to send to the FTP Server.
        """
        msg += "\r\n"
        self.server_socket.sendall(msg.encode('utf-8'))

    def user_command(self, username):
        """
        User Name
        "The user identification is that which is required by the server for access to its file system."
        :param username: Telnet string identifying the user
        """
        command = "USER " + username
        self.send_to_server(command)

    def pass_command(self, password):
        """
        Password
        "This command must be immediately preceded by the user name command, and, for some sites,
        completes the user’s identification for access control."
        :param password: Telnet string specifying the user’s password
        """
        command = "PASS " + password
        self.send_to_server(command)

    def cwd_command(self, pathname):
        """
        Change Working Directory
        "This command allows the user to work with a different
        directory or dataset for file storage or retrieval without
        altering his login or accounting information."
        :param pathname: pathname specifies a directory or other system dependent
        file group designator
        """
        command = "CWD " + pathname
        self.send_to_server(command)

    def quit_command(self):
        """
        Logout
        "This command terminates a USER and if file transfer is not
        in progress, the server closes the control connection. If
        file transfer is in progress, the connection will remain
        open for result response and the server will then close it."
        """
        self.send_to_server("QUIT")

    def pasv_command(self):
        """
        Passive Mode
        "This command requests the server-DTP to "listen" on a data
        port (which is not its default data port) and to wait for a
        connection rather than initiate one upon receipt of a
        transfer command. The response to this command includes the
        host and port address this server is listening on."
        """
        self.send_to_server("PASV")

    def epsv_command(self):
        """
        Extended Passive Mode
        """
        self.send_to_server("EPSV")

    def port_command(self, port):
        """
        Data Port
        "The argument is a HOST-PORT specification for the data port
        to be used in data connection. There are defaults for both
        the user and server data ports, and under normal
        circumstances this command and its reply are not needed."
        :param port: TCP Port to connect to
        """
        command = "PORT " + port
        self.send_to_server(command)

    def eprt_command(self, netport, netaddr, tcpport):
        """
        "The EPRT command allows for the specification of an extended address
        for the data connection.  The extended address MUST consist of the
        network protocol as well as the network and transport addresses"
        - https://tools.ietf.org/html/rfc2428

        :param netport:
        :param netaddr:
        :param tcpport:
        """
        command = "EPRT |" + netport + "|" + netaddr + "|" + tcpport + "|"
        self.send_to_server(command)

    def retr_command(self, pathname):
        """
        "This command causes the server-DTP to transfer a copy of the
        file, specified in the pathname, to the server- or user-DTP
        at the other end of the data connection."

        :param pathname: file specified by pathname
        """
        command = "RETR " + pathname
        self.send_to_server(command)

    def stor_command(self, pathname):
        """
        "This command causes the server-DTP to accept the data
        transferred via the data connection and to store the data as
        a file at the server site. If the file specified in the
        pathname exists at the server site, then its contents shall
        be replaced by the data being transferred. A new file is
        created at the server site if the file specified in the
        pathname does not already exist."

        :param pathname: path to store the file
        """
        command = "STOR " + pathname
        self.send_to_server(command)

    def pwd_command(self):
        """
        Print Working Directory
        "This command causes the name of the current working
        directory to be returned in the reply."
        """
        self.send_to_server("PWD")

    def syst_command(self):
        """
        "This command is used to find out the type of operating
        system at the server. The reply shall have as its first
        word one of the system names listed in the current version
        of the Assigned Numbers document"
        """
        self.send_to_server("SYST")

    def list_command(self, pathname):
        """
        "This command causes a list to be sent from the server to the
        passive DTP. If the pathname specifies a directory or other
        group of files, the server should transfer a list of files
        in the specified directory. If the pathname specifies a
        file then the server should send current information on the
        file. A null argument implies the user’s current working or
        default directory."

        :param pathname: (optional, pass "" if current working/default directory)
            pathname to send list
        """
        command = "LIST " + pathname
        self.send_to_server(command)

    # TODO current bug -
    #  specifying a command to HELP with does not return specific help for that command
    def help_command(self, cmd):
        """
        "This command shall cause the server to send helpful
        information regarding its implementation status over the
        control connection to the user."

        :param cmd: (optional, pass "" if not needed.) command to look up
        """
        command = "HELP " + cmd
        self.send_to_server(command)


if __name__ == '__main__':
    ftp = FTPConnection()
    ftp.connect_to_server("10.246.251.93", 21)
    print(ftp.get_server_response())
    ftp.user_command("cs472")
    print(ftp.get_server_response())
    ftp.pass_command("hw2ftp")
    print(ftp.get_server_response())
