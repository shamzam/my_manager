from psycopg2.sql import Identifier, Literal, SQL


class COLUMN:

    def __init__(
        self,
        name: Identifier,
        type: str,
        length: int = 0,
        default_value: str = "",
        primary_key: bool = False,
        not_null: bool = False
    ):
        self.name = Identifier(name)
        self.type = type
        self.length = length
        self.vals: list[str] = []
        self.defaultValue = default_value
        self.primary_key = primary_key
        self.not_null = not_null
        self.table_alias = Identifier("m1")
        self.alias = ""

    def __repr__(self):
        return self.name + " " + self.type + ("(" + self.length + ")" if self.length != 0 else "") + " "

    def AS(self, alias: str):
        self.alias = alias

        return self

    def get_full_sql(self):
        return SQL("{table_alias}.{name}").format(table_alias=self.table_alias, name=self.name)
