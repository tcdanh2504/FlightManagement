class Result:
    def __init__(self, data=None, error=None):
        self.data = data
        self.error = error

    def is_success(self):
        return self.error is None