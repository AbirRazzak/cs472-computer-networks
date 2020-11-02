__EXAMPLE_USER_BASE__ = {
    "user1": "pass123",
    "user2": "pass123",
    "user3": "pass123",
    "user4": "pass123"
}


def auth_user(username, password):
    if username in __EXAMPLE_USER_BASE__:
        return password == __EXAMPLE_USER_BASE__[username]
    else:
        return False
