"""
generate sample employee data
"""

from yoyo import step

__depends__ = {'20240604_02_n6kZK-rename-employee-table'}

steps = [
    step(
        """
        INSERT INTO employees (first_name, last_name, nickname, department) values
            ('Isaac', 'Newton', null, 'Physics'),
            ('Albert', 'Einstein', null, 'Physics'),
            ('John', 'von Neumann', 'Johnny', 'Mathematics'),
            ('Joseph', 'Fourier', 'Joe', 'Mathematics'),
            ('Blaise', 'Pascal', null, 'Mathematics'),
            ('John', 'Cleese', null, 'Drama'),
            ('William', 'Shakespeare', 'Willie', 'English Lit')
        ;
        """,
        "DELETE FROM employees;"
    )
]
