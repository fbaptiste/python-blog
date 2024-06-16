"""
rename employee table
"""

from yoyo import step

__depends__ = {'20240604_01_u0XKn-db-init'}

steps = [
    step(
        "ALTER TABLE employee RENAME TO employees;",
        "ALTER TABLE employees RENAME TO employee;",
    ),
]
