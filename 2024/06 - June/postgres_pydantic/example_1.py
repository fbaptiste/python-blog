"""Example 1"""
# embedding configs here to keep things simple
# never do this in actual code - especially if it gets committed to a VCS
from dataclasses import dataclass

import psycopg
from psycopg.rows import dict_row, namedtuple_row, class_row
from pydantic import BaseModel, Field


POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "mathbyte"
POSTGRES_USER = "admin"
POSTGRES_PWD = "secret"


@dataclass
class DCEmployee:
    id: int
    first_name: str
    last_name: str
    nickname: str
    department_id: int


class Employee(BaseModel):
    employee_id: int = Field(alias="id")
    first_name: str
    last_name: str
    nickname: str | None = None
    department_id: int


def run_query_tuple(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM employees;")
        rows = cur.fetchall()

    print("Standard Default Return")
    print("=" * 50)
    if rows:
        print(f"type(row)={type(rows[0])}")
    for row in rows:
        print(row)
    print("\n")


def run_query_with_factory(conn, row_factory):
    with conn.cursor(row_factory=row_factory) as cur:
        cur.execute("SELECT * FROM employees;")
        rows = cur.fetchall()

    print(f"{row_factory.__name__} Factory")
    print("=" * 50)
    if rows:
        print(f"type(row)={type(rows[0])}")
    for row in rows:
        print(row)
    print("\n")


if __name__ == "__main__":
    conn_str = (
        f"host={POSTGRES_HOST} "
        f"port={POSTGRES_PORT} "
        f"dbname={POSTGRES_DB} "
        f"user={POSTGRES_USER} "
        f"password={POSTGRES_PWD}"
    )

    with psycopg.connect(conn_str) as conn:
        # example 1: return data as a tuple
        run_query_tuple(conn)

        # example 2: return data as a named tuple
        run_query_with_factory(conn, namedtuple_row)

        # example 3: return data as a Python dict
        run_query_with_factory(conn, dict_row)

        # example 4: return data as a custom dataclass
        run_query_with_factory(conn, class_row(DCEmployee))

        # example 5: return data as a custom Pydantic model
        run_query_with_factory(conn, class_row(Employee))