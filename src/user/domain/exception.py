from shared.domain.exception import NotFoundException


class UserNotFoundException(NotFoundException):
    model_name = "User"
