

class APIError(Exception):
    
    def __init__(self, status=400, msg='', code=0):
        self.status = status
        self.msg = msg
        self.code = code


