import psycopg2
import psycopg2.errors as Errors
from psycopg2.sql import Composable, Identifier, Literal, SQL
from psycopg2.extras import DictCursor, DictConnection

from .COLUMN import COLUMN
from .CONFIG import Config
from .ORMError import ORMError
from ..DBUtils.Types import DB_ER_DUPLICATE


class BASE():

    query: Composable
    table: Identifier
    schema: Identifier
    alias: Identifier

    def get_dsn(self):
        config = Config()
        config.read_config("./my_manager.ini")

        return f"host={config.db_host} dbname={config.db_name} user={config.db_user} password={config.db_pass} port={config.db_port}"

    def __init__(self, table: str, schema: str = "public", alias: str = "m1"):
        self.table = Identifier(table)
        self.schema = Identifier(schema)
        self.alias = Identifier(alias)
        self.query = SQL("")
        self.columns: dict[COLUMN] = {
            name: getattr(self, name) for name, type in self.__annotations__.items() if "COLUMN" in str(type)}
        self.set_table_alias()

    def AS(self, alias: str):
        self.alias = Identifier(alias)
        self.set_table_alias()

        return self

    def set_table_alias(self):
        for column in self.columns:
            getattr(self, column).table_alias = self.alias

    def INNERJOIN(self, base):
        self.query = SQL("{query} INNER JOIN {table}").format(
            query=self.query,
            table=self.get_table_name(base, has_alias=True)
        )

        return self

    def LEFTJOIN(self, base):
        self.query = SQL("{query} LEFT JOIN {table}").format(
            query=self.query,
            table=self.get_table_name(base, has_alias=True)
        )

        return self

    def RIGHTJOIN(self, base):
        self.query = SQL("{query} RIGHT JOIN {table}").format(
            query=self.query,
            table=self.get_table_name(base, has_alias=True)
        )

        return self

    def FULLJOIN(self, base):
        self.query = SQL("{query} FULL OUTER JOIN {table}").format(
            query=self.query,
            table=self.get_table_name(base, has_alias=True)
        )

        return self

    def INSERT(self, column_list: list[COLUMN] = [], value_list: list[str] = []):
        self.query = SQL("INSERT INTO {table} ({columns}) VALUES ({values});").format(
            table=self.get_table_name(self),
            columns=self.get_column_names(column_list),
            values=self.get_values(value_list)
        )

        return self

    def UPDATE(self, column_list: list[COLUMN] = [], value_list: list[str] = []):
        self.query = SQL("UPDATE {table} SET {update}").format(
            table=self.get_table_name(self, has_alias=True),
            update=SQL(", ").join([SQL("{column}={value}").format(
                column=column.name,
                value=Literal(value_list[i])
            ) for i, column in enumerate(column_list)])
        )

        return self

    def DELETE(self):
        self.query = SQL("DELETE FROM {table}").format(
            table=self.get_table_name(self, has_alias=True))

        return self

    def SELECT(self, column_list: list[COLUMN] = []):
        self.query = SQL("SELECT {columns} FROM {table}").format(
            columns=self.get_column_names(column_list, has_alias=True),
            table=self.get_table_name(self, has_alias=True)
        )

        return self

    def WHERE(self):
        self.query = SQL("{query} WHERE").format(query=self.query)

        return self

    def ON(self):
        self.query = SQL("{query} ON").format(query=self.query)

        return self

    def AND(self):
        self.query = SQL("{query} AND").format(query=self.query)

        return self

    def OR(self):
        self.query = SQL("{query} OR").format(query=self.query)

        return self

    def EQ(self, column: COLUMN, value: str | COLUMN):
        self.query = SQL("{query} {column}={value}").format(
            query=self.query, column=column.get_full_sql(), value=Literal(value) if type(value) is str else value.get_full_sql()
        )

        return self

    def LT(self, column: COLUMN, value: str | COLUMN, eq: bool = False):
        self.query = SQL("{query} {column}<" + ("=" if eq else "") + "{value}").format(
            query=self.query, column=column.get_full_sql(), value=Literal(value) if type(value) is str else value.get_full_sql()
        )

        return self

    def GT(self, column: COLUMN, value: str | COLUMN, eq: bool = False):
        self.query = SQL("{query} {column}>" + ("=" if eq else "") + "{value}").format(
            query=self.query, column=column.get_full_sql(), value=Literal(value) if type(value) is str else value.get_full_sql()
        )

        return self

    def get_table_name(self, base, has_alias: bool = False):
        return SQL("{schema}.{tableName}" + (" AS {alias}" if has_alias else "")).format(
            schema=base.schema,
            tableName=base.table,
            alias=base.alias
        )

    def get_column_names(self, column_list: list[COLUMN] = [], has_alias: bool = False):
        if len(column_list) == 0:
            column_list = [self.columns[column] for column in self.columns]
        if has_alias:
            return SQL(", ").join([
                SQL("{column} as {alias}").format(
                    column=column.get_full_sql(),
                    alias=Identifier(column.alias)
                ) if column.alias != "" else column.get_full_sql() for column in column_list
            ])
        else:
            return SQL(", ").join([
                SQL("{column} as {alias}").format(
                    column=column.name,
                    alias=Identifier(column.alias)
                ) if column.alias != "" else column.name for column in column_list
            ])

    def get_values(self, value_list: list[str] = []):
        return SQL(",").join([Literal(value) for value in value_list])

    def print_sql(self):
        with psycopg2.connect(self.get_dsn()) as conn:
            print(self.query.as_string(conn))

    def execute(self):
        try:
            with psycopg2.connect(self.get_dsn()) as conn:
                with conn.cursor() as cur:
                    cur.execute(self.query)
        except Errors.UniqueViolation as e:
            raise ORMError(DB_ER_DUPLICATE, str(e))

    def fetchAll(self):
        result = []
        with psycopg2.connect(self.get_dsn(), connection_factory=DictConnection) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    self.query)
                data = cur.fetchall()
                for row in data:
                    result.append(dict(row))

        return result
