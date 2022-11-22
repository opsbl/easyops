class ValidError(Exception):
    def __init__(self, code, message="", data=None):
        self.code = code
        self.message = message
        self.data = data

    def __str__(self):
        return self.message
