import input
import output
import ftp
import logger
import dnsresolver


class Middleman:
    # Class Middleman - Object in charge of connecting the command line args to the ftp server
    conn = None
    log_file = None

    def __init__(self, servername, log_path, port):
        self.conn = ftp.FTPConnection()
        self.log_file = logger.Logger(log_path)
        self.connect(servername, port)

    def connect(self, servername, port):
        """
        Establishes the connection to the FTP Server
        :param servername: FTP Server Name (can be host name or ip address)
        :param port: Port number to connect to the server
        """
        # If FTP server host is non-numeric, use a DNS resolver to fetch the IP address
        ip = dnsresolver.lookup_ipaddr(servername)
        self.log_and_display_message("Connecting to {0} ({1}).".format(servername, ip))
        self.conn.connect_to_server(ip, port)
        self.log_and_display_server_response()

    def main_loop(self):
        """
        Asks the user for a command and processes the inputs to a command on the FTP Server
        """
        loop = True
        while loop:
            output.display("Select a command:")
            output.display("1. Login As User")  # user/pass
            output.display("2. Change Current Directory")  # cwd
            output.display("3. Check Current Directory")  # pwd
            output.display("4. Enter Passive Mode")  # pasv
            output.display("5. Enter Extended Passive Mode")  # epsv
            output.display("6. Retrieve File")  # retr
            output.display("7. Store File")  # stor
            output.display("8. Send List to Passive DTP")  # list
            output.display("9. Specify Extended Address")  # eprt
            output.display("10. Change Port Number")  # port
            output.display("11. Check Operating System of Server")  # syst
            output.display("12. Help")  # help
            output.display("13. Exit FTP Connection")  # exit

            option = input.retrieve()

            if option == '1':
                self.login()
            elif option == '2':
                self.cwd()
            elif option == '3':
                self.pwd()
            elif option == '4':
                self.pasv()
            elif option == '5':
                self.epsv()
            elif option == '6':
                self.retrieve()
            elif option == '7':
                self.store()
            elif option == '8':
                self.list()
            elif option == '9':
                self.eprt()
            elif option == '10':
                self.port()
            elif option == '11':
                self.syst()
            elif option == '12':
                self.help()
            elif option == '13':
                self.quit()
                loop = False
            else:
                pass

    def login(self):
        """
        Logs into the FTP Server. Uses the USER and PASS commands to do so.
        """
        # Send USER
        output.display("Enter Username")
        user = input.retrieve()
        self.conn.user_command(user)
        self.log_and_display_message("Sent: USER {0}".format(user))
        self.log_and_display_server_response()
        # Send PASS
        output.display("Enter Password")
        passwd = input.retrieve_private()
        self.conn.pass_command(passwd)
        self.log_and_display_message("Sent: PASS")
        self.log_and_display_server_response()

    def cwd(self):
        """
        Changes the current directory. Uses the CWD command to do so.
        """
        output.display("Enter Path")
        path = input.retrieve()
        self.conn.cwd_command(path)
        self.log_and_display_message("Sent: CWD {0}".format(path))
        self.log_and_display_server_response()

    def pwd(self):
        """
        Gets the current directory. Uses the PWD command to do so.
        """
        self.conn.pwd_command()
        self.log_and_display_message("Sent: PWD")
        self.log_and_display_server_response()

    def pasv(self):
        """
        Enters Passive Mode. Uses the PASV command to do so.
        """
        self.conn.pasv_command()
        self.log_and_display_message("Sent: PASV")
        self.log_and_display_server_response()

    def epsv(self):
        """
        Enters Extended Passive Mode. Uses the EPSV command to do so.
        """
        self.conn.epsv_command()
        self.log_and_display_message("Sent: EPSV")
        self.log_and_display_server_response()

    def retrieve(self):
        """
        Uses the FTP Server to retrieve files. Uses the RETR command to do so.
        """
        output.display("Specify the pathname to the file.")
        pathname = input.retrieve()
        self.conn.retr_command(pathname)
        self.log_and_display_message("Sent: RETR {0}".format(pathname))
        self.log_and_display_server_response()

    def store(self):
        """
        Uses the FTP Server to store files. Uses the STOR command to do so.
        """
        output.display("Specify the pathname to save the file.")
        pathname = input.retrieve()
        self.conn.stor_command(pathname)
        self.log_and_display_message("Sent: STOR {0}".format(pathname))
        self.log_and_display_server_response()

    def list(self):
        """
        Sends a list to a passive DTP using the FTP Server. Uses the LIST command to do so.
        """
        output.display("Enter the pathname to send as a list.")
        listpath = input.retrieve()
        self.conn.list_command(listpath)
        self.log_and_display_message("Sent: LIST {0}".format(listpath))
        self.log_and_display_server_response()

    def eprt(self):
        """
        Specifies an extended address for the FTP Server. Uses the EPRT command to do so.
        """
        output.display("Enter the net port to connect to.")
        netprt = input.retrieve()
        output.display("Enter the net address to connect to.")
        netaddr = input.retrieve()
        output.display("Enter the tcp port to connect to.")
        tcpprt = input.retrieve()
        self.conn.eprt_command(netprt, netaddr, tcpprt)
        self.log_and_display_message("Sent: EPRT |{0}|{1}|{2}|".format(netprt, netaddr, tcpprt))
        self.log_and_display_server_response()

    def port(self):
        """
        Specifies the port for the FTP Server. Uses the PORT command to do so.
        """
        output.display("Enter the port number to connect to.")
        port = input.retrieve()
        self.conn.port_command(port)
        self.log_and_display_message("Sent: PORT {0}".format(port))
        self.log_and_display_server_response()

    def syst(self):
        """
        Asks the FTP Server what operating system it is running. Uses the SYST command to do so.
        """
        self.conn.syst_command()
        self.log_and_display_message("Sent: SYST")
        self.log_and_display_server_response()

    def help(self):
        """
        Asks the FTP Server for help on various commands. Uses the HELP command to do so.
        """
        output.display("Enter a command to lookup. Leave blank if general help.")
        command = input.retrieve()
        self.conn.help_command(command)
        self.log_and_display_message("Sent: HELP {0}".format(command))
        self.log_and_display_server_response()

    def quit(self):
        """
        Quits the current FTP Server. Uses the QUIT command to do so.
        """
        self.conn.quit_command()
        self.log_and_display_message("Sent: QUIT")

    def log_and_display_message(self, msg):
        """
        Helper function. Logs and displays a single message.
        :param msg: Message to log into the log file, and display on the output
        """
        self.log_file.log(msg)
        output.display(msg)

    def log_and_display_server_response(self):
        """
        Helper function. All current server responses are logged to the log file and displayed on the output.
        """
        response = self.conn.get_server_response()
        for msg in response:
            self.log_file.log("Received: " + msg)
            output.display(msg)