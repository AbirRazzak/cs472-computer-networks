import output


def get_config_attribute(attribute):
    try:
        file = open("ftpserverd.conf", "r")
        for line in file:
            search_term = attribute + ' = '
            if line.startswith(search_term):
                split = line.split(' = ')
                return split[1].strip('\n')
        file.close()
        return None
    except OSError:
        output.display('Error reading config file. Check that ftpserverd.conf exists.')


def check_for_config():
    try:
        file = open("ftpserverd.conf", "r")
        file.close()
        return True
    except OSError:
        return False
