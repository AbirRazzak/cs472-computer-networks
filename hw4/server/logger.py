from datetime import datetime


def format_log_msg(time, msg):
    """
    Formats a time and message into a log file output
    :param time: string of the current time
    :param msg: string of the message
    :return: log file output in "10/01/2020 22:00:00.0031 Sent: USER cs472" format
    """
    log_format = '{0} {1}\n'
    formatted = log_format.format(time, msg)
    return formatted


def get_current_time():
    """
    Formats the current time and returns it
    :return: Current time formatted in "10/01/2020 22:00:00.0002" format
    """
    curr_time = datetime.now()
    time_formatted = curr_time.strftime('%m/%d/%Y %H:%M:%S.%f')
    return time_formatted


class Logger:
    # Class Logger - in charge of handling writing all log outputs to a specified filepath.
    filename = ""

    def __init__(self, pathname):
        self.filename = pathname

    def log(self, msg):
        """
        Formats given message and logs it to a file.
        :param msg: string to save to log file
        :param filename: filename of the log file to save to
        """
        formatted_msg = format_log_msg(get_current_time(), msg)
        self.append_to_file(formatted_msg)

    def append_to_file(self, text):
        """
        Helper function
        Writes to the end of a file and then closes it.
        :param text: string of text to add to file
        :param filename: filename of the file to write to
        """
        file = open(self.filename, 'a')
        file.write(text)
        file.close()
