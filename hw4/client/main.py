import output
import sys
import middleman

__DEFAULT_PORT__ = 21


def check_num_args():
    """
    Checks to make sure the correct number of command line args are given.
    """
    num_args = len(sys.argv)
    if num_args < 2:
        output.display("Not enough arguments are supplied.")
        sys.exit(1)
    if num_args > 4:
        output.display("Too many argument are supplied.")
        sys.exit(1)


def sanitize_args():
    """
    Helper function. Checks command line args to make sure proper values are given.
    """
    # Check that the given port number is an integer
    if len(sys.argv) is 4:
        try:
            int(sys.argv[3])
        except ValueError:
            output.display("Port number must be an integer.")
            sys.exit(1)


def start():
    """
    Starts the main loop of the program.
    """
    # if port number is not given, use the default port number
    if len(sys.argv) is 4:
        port = sys.argv[3]
    else:
        port = __DEFAULT_PORT__
    processor = middleman.Middleman(sys.argv[1], sys.argv[2], port)
    processor.main_loop()


if __name__ == '__main__':
    check_num_args()
    sanitize_args()
    start()
