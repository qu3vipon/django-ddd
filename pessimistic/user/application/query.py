from user.infra.database.repository.rdb import UserRDBRepository


class UserQuery:
    def __init__(self, user_repo: UserRDBRepository):
        self.user_repo = user_repo

    def get_user(self, user_id: int):
        return self.user_repo.get_user_by_id(user_id=user_id)
