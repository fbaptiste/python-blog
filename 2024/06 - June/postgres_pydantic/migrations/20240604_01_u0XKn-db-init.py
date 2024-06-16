"""
db init
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE employee (
            id SERIAL PRIMARY KEY,
            first_name text NOT NULL,
            last_name text NOT NULL,
            nickname text,
            department text NOT NULL
        );
        """,
        "DROP TABLE employee;"
    )
]
