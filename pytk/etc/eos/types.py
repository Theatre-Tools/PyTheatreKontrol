from enum import Enum

class EosGet(Enum):
    ## A response class for every type of get command, will contain an HTML style status code, and a body.
    def __init__(self, status_code: int, body: tuple):
        self.status_code = status_code
        self.body = body