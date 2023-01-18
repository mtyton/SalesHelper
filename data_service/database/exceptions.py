
class ValidationError(Exception):
    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop("message")
        super().__init__(*args, **kwargs) 


class DocumentAlreadyExistsException(Exception):
    ...
