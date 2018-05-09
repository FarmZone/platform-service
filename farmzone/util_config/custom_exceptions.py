from rest_framework.exceptions import APIException, ValidationError


class CustomAPI404Exception(APIException):
    status_code = 200

    def __init__(self, detail=None):
        if isinstance(detail, dict):
            self.response = detail
            self.response.update({'status':self.status_code})
        else:
            self.response = {
                "detail": detail,
                "status_code": self.status_code
            }
        super(CustomAPI404Exception, self).__init__(detail, self.status_code)


class CustomAPI400Exception(APIException):
    status_code = 200

    def __init__(self, detail):
        if isinstance(detail, dict):
            self.response = detail
            self.response.update({'status':self.status_code})
        else:
            self.response = {
                "detail": detail,
                "status_code": self.status_code
            }
        super(CustomAPI400Exception, self).__init__(detail, self.status_code)


class MissingRequiredField(CustomAPI400Exception):
    def __init__(self, detail):
        super(MissingRequiredField, self).__init__(detail)


class InvalidInput(CustomAPI400Exception):
    def __init__(self, detail):
        super(InvalidInput, self).__init__(detail)


class InvalidRequest(CustomAPI400Exception):
    def __init__(self, detail):
        super(InvalidRequest, self).__init__(detail)
