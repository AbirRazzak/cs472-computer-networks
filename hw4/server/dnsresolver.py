import socket


def lookup_ipaddr(hostname):
    """
    Looks up the IP Address from a hostname.
    :param hostname: Hostname to look up
    :return: IP Address of the hostname
    """
    return socket.gethostbyname(hostname)
