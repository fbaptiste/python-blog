"""
change departments to FK
"""

from yoyo import step

__depends__ = {'20240604_03_sYLbA-generate-sample-employee-data'}

steps = [
    step(
        "CREATE TABLE departments (id SERIAL PRIMARY KEY, name text);",
        "DROP TABLE departments;"
    ),
    step(
        "INSERT INTO departments (name) SELECT distinct department from employees;",
        "DELETE FROM departments;"
    ),
    step(
        "ALTER TABLE employees ADD COLUMN department_id integer;",
        "ALTER TABLE employees DROP COLUMN department_id;"
    ),
    step(
        """
        UPDATE employees 
        SET department_id=departments.id 
        FROM departments 
        WHERE employees.department = departments.name;
        """,
        "UPDATE employees set department_id = null;"
    ),
    step(
        "ALTER TABLE employees DROP COLUMN department;",
        """
            ALTER TABLE employees ADD COLUMN department text;
            UPDATE employees
            SET department = departments.name
            FROM departments
            WHERE employees.department_id = departments.id;
        """
    ),
    step(
        """
        ALTER TABLE employees
        ADD CONSTRAINT fk_employees_departments FOREIGN KEY (department_id) REFERENCES departments (id);
        """,
        """ALTER TABLE employees DROP CONSTRAINT fk_employees_departments;"""
    )
]
