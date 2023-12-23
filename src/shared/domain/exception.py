class BaseMsgException(Exception):
    message: str

    def __str__(self):
        return self.message


class NotFoundException(Exception):
    model_name: str

    def __str__(self):
        return f"{self.model_name} Not Found"
