from DAO.usersDAO import DBUsers
from models.usersModels import User
from ORM.DBObjects import ORMError


def login(user_id: str, password: str):
    db_users = DBUsers()
    db_users.SELECT().WHERE().EQ(db_users.user_id, user_id).AND().EQ(
        db_users.password, password)
    user = db_users.fetchAll()[0]
    return user


def register_user(user: User):
    try:
        db_users = DBUsers()
        db_users.INSERT(
            [db_users.user_id, db_users.password,
                db_users.username, db_users.role, db_users.email],
            [user.user_id, user.password, user.username, user.role, user.email]
        )
        db_users.execute()

        return {"data": user, "error_code": 0, "error_detail": ""}

    except ORMError as e:
        return {"data": None, "error_code": e.error_code, "error_detail": e.error_detail}


def update_user(user: User, former_user_id: str):
    try:
        db_users = DBUsers()
        db_users.UPDATE(
            [db_users.user_id, db_users.password,
                db_users.username, db_users.role, db_users.email],
            [user.user_id, user.password, user.username, user.role, user.email]
        ).WHERE().EQ(db_users.user_id, former_user_id)
        db_users.print_sql()
        db_users.execute()

        return {"data": user, "error_code": 0, "error_detail": ""}

    except ORMError as e:
        return {"data": None, "error_code": e.error_code, "error_detail": e.error_detail}


def delete_user(user: User):
    try:
        db_users = DBUsers()
        db_users.DELETE().WHERE().EQ(db_users.user_id, user.user_id)

        return {"data": user, "error_code": 0, "error_detail": ""}

    except ORMError as e:
        return {"data": None, "error_code": e.error_code, "error_detail": e.error_detail}
