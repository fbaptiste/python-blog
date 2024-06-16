"""Example 2"""
# embedding configs here to keep things simple
# never do this in actual code - especially if it gets committed to a VCS

import psycopg
from psycopg.rows import dict_row, namedtuple_row, class_row
from pydantic import BaseModel, Field


POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "mathbyte"
POSTGRES_USER = "admin"
POSTGRES_PWD = "secret"


class Employee(BaseModel):
    employee_id: int = Field(alias="id")
    first_name: str
    last_name: str
    nickname: str | None = None
    department: str


if __name__ == "__main__":
    conn_str = (
        f"host={POSTGRES_HOST} "
        f"port={POSTGRES_PORT} "
        f"dbname={POSTGRES_DB} "
        f"user={POSTGRES_USER} "
        f"password={POSTGRES_PWD}"
    )

    with psycopg.connect(conn_str) as conn:
        with conn.cursor(row_factory=class_row(Employee)) as cur:
            cur.execute("""
                SELECT employees.id, 
                    employees.first_name, 
                    employees.last_name, 
                    employees.nickname, 
                    departments.name as department
                FROM employees 
                INNER JOIN departments on employees.department_id=departments.id
                ORDER BY last_name;
            """)
            rows = cur.fetchall()

        for row in rows:
            print(row)
