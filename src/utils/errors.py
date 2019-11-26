class Error(Exception):

    def __init__(self, err_msg, err_code=None, status=500,
                 context=None, reason=None):

        self.err_code = err_code or "errors.internalError"
        self.err_msg = err_msg or "Internal error occured please contact your admin"
        self.status = status
        self.context = context or {}
        self.reason = reason