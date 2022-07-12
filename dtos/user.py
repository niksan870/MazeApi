class UserDTO:
    __slots__ = ("name", "password", "public_id")

    def __init__(self, name, password, public_id=None):
        self.public_id = public_id
        self.password = password
        self.name = name
