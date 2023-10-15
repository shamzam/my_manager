class ORMError(Exception):

    def __init__(self, error_code: int, error_detail: str):
        super().__init__()
        self.error_code = error_code
        self.error_detail = error_detail
