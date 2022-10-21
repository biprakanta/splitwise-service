class ServiceException(Exception):
    detail = "Bad Request"

    def __init__(self, detail: str):
        if detail is not None:
            self.detail = detail


class DuplicateMobileException(ServiceException):
    detail = "Mobile already exists"


class DoesNotExist(ServiceException):
    detail = "Entity not found"
