from ORM.DBUtils import Types
from ORM.DBObjects import COLUMN, BASE


class DBUsers(BASE):

    user_id: COLUMN
    password: COLUMN
    username: COLUMN
    role: COLUMN
    email: COLUMN

    def __init__(self):
        self.user_id: COLUMN = COLUMN("user_id", Types.CL_T_VARCHAR,
                                      50, primary_key=True, not_null=True)
        self.password: COLUMN = COLUMN("password", Types.CL_T_VARCHAR,
                                       50, not_null=True)
        self.username: COLUMN = COLUMN("username", Types.CL_T_VARCHAR,
                                       50, not_null=True)
        self.role: COLUMN = COLUMN("role", Types.CL_T_INT, not_null=True)
        self.email: COLUMN = COLUMN("email", Types.CL_T_VARCHAR, 50)
        super().__init__("users")
