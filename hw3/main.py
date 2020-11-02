import sys
import output
import socket
import logger
import threading
import server


__TIMEOUT__ = 1.0
__STACK_SIZE__ = 5


def check_num_args():
    """
    Checks to make sure the correct number of command line args are given.
    """
    num_args = len(sys.argv)
    if num_args < 3:
        output.display("Not enough arguments are supplied.")
        sys.exit(1)
    if num_args > 3:
        output.display("Too many argument are supplied.")
        sys.exit(1)


def sanitize_args():
    """
    Helper function. Checks command line args to make sure proper values are given.
    """
    # Check that the given port number is an integer
    try:
        int(sys.argv[2])
    except ValueError:
        output.display("Port number must be an integer.")
        sys.exit(1)


def start():
    """
    Starts the main loop of the program.
    """
    threadLock = threading.Lock()
    threads = []

    server_logger = logger.Logger(sys.argv[1])
    server_socket = create_socket()
    msg = "Starting FTP Server on {0}:{1}".format(socket.gethostbyname(socket.gethostname()), int(sys.argv[2]))
    display_and_log(msg, server_logger)

    while True:
        try:
            (client, addr) = server_socket.accept()
            msg = "New client connection from {0}:{1}".format(addr[0], addr[1])
            display_and_log(msg, server_logger)

            server_thread = server.FTPServer(client, addr, server_logger)
            server_thread.start()
            threads.append(server_thread)
        except KeyboardInterrupt:
            # CTRL+C to exit the server loop and shut down
            break
        except socket.timeout:
            # If the socket times out, just loop again
            # This is so that the server can take some time to read for KeyboardInterrupt (CTRL+C)
            pass
        except Exception as ex:
            # An unknown error occurs, log it to the log file
            display_and_log("Error thrown on server! Error: {0}".format(ex), server_logger)
            # break

    # Wait for all threads to complete
    for t in threads:
        t.join()
    server_socket.close()
    display_and_log("Exiting Server", server_logger)
    sys.exit(0)


def display_and_log(msg, slogger: logger.Logger):
    """
    Displays the msg to the output and also logs it using a logger object
    :param msg: Message to display/log
    :param slogger: Server Logger
    """
    output.display(msg)
    slogger.log(msg)


def create_socket():
    """
    Creates a server socket using the port defined by sys arg 2, with a backlog of global variable __STACK_SIZE__
    :return: New server socket to listen for client messages on
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), int(sys.argv[2])))
    server_socket.settimeout(__TIMEOUT__)
    server_socket.listen(__STACK_SIZE__)
    return server_socket


if __name__ == '__main__':
    check_num_args()
    sanitize_args()
    start()
