import getpass


def retrieve():
    """
    Retrieves an input from the user.
    :return: User's input
    """
    r = input()
    return r


def retrieve_private():
    """
    Privately retrieves an input from the user.
    :return: User's input
    """
    p = getpass.getpass()
    return p
