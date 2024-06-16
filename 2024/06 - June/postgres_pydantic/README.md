# Integrating Python and Postgres

## Introduction
In this series of videos, I will show you how to set up a local Postgres database using docker compose, how to
version you database structure using what is called a migration tool, and lastly how to query your database
from Python and leverage Pydantic to model your table structures.

No ORMs needed!! In fact, I'm going to make a statement that many people will find horrendous - I abhor ORMs. I happen
to like SQL, and am good at it. I find SQL is perfect for querying structured relational data in an RDBMS. ORMs? Not
so much. You have to perform a great deal of contortions in order to "generate" equivalent SQL queries. And now, I have
to learn a huge amount of extra stuff just so I can create tables and query data from SQL - something I already know,
and can do in my sleep (ok, I'm exaggerating a bit!), using plain SQL syntax.

Now that said, ORMs can be very useful - an ORM such as SQLAlchemy can essentially be database-agnostic - it is equally
at home with Postgres as it is with SQL Server, MariaDB, and many others. When you use SQL, you usually have to
use the specific SQL dialect corresponding to the database server you are using.

But, in all honesty, when you build systems, are you really building a system that can seamlessly be configured
to switch which database it is "talking" to? Or do you usually have some single database platform you are using? 
In my case, when I start a project, I already know what database platform I am going to use, and that's not going to 
change over the lifetime of the project. So, plain SQL it is - I know it well, and I don't have to learn a 
complicated humongous ORM (and it has to be, by necessity, since it needs to be a jack of all trades).

One thing an ORM also gives you that is useful, is something that addresses the so-called "impedance mismatch".

In Python code, data is usually represented by classes, whereas in SQL, data is essentially rows (or tuples) of data.

When you query data from a database, ORMs do this "translation" from the raw SQL data to your Python objects 
automagically.

However, the Postgres library `psycopg` gives us the ability to do the same thing **very easily**, without resorting
to an ORM. And in this series of videos I'll show you how you can leverage Pydantic or plain data classes to 
handle this "impedance mismatch".

If however, you are adamant about using an ORM such SQLAlchemy, then, to paraphrase Obi Wan Kenobi, this is not 
the video you are looking for! Or, in other words, "move along, nothing to see here!". However, if you're like
me, and would rather not have to learn an ORM such as SQLAlchemy, then stick around - I'll show you how!


## Setting up your dev environment
All the code and examples I am going to show you in this series is being run on a Mac. If you use Linux things should
pretty much be the same. For Windows you may have to adjust a few things here and there - please don't ask me for 
Windows support - I have not used that operating system for development in over a decade!!

First thing is you should install Docker on your machine if you have not already. 

Next, we need to set up our Python virtual environment.

We are going to need a few things to work with Postgres.

One package we will need is for our Python code to connect to Postgres and execute queries - we will use the `psycopg`
library for that - normally for API projects I would use connection pooliong, but for these simple examples
I'll skip that and just use a regular connection.

Another package we will use is to create data structures in a Postgres database (such as tables, indexes, views and 
so on). Although you can certainly use a 3rd party query tool to create your database structure, a preferred practice 
is to do so using code - that way you can version your database as it changes over time.

My tool of choice for this is a simple one called `yoyo`. Documentation for it is available 
[here](https://ollycope.com/software/yoyo/latest/), but I'll show you how to use it in this and upcoming videos.

Lastly, we'll also need to Pydantic, so you'll need to install that too.

So, the packages you should install are:

- `psycopg[binary]`
- `yoyo-migrations`
- `pydantic`

The `psycopg` library needs various binaries - most OS's and Python versions have pre-compiled binaries available, 
which you can install using `pip install psycopg[binary]`. If you get errors and the binaries are not available
for you for some reason, you'll need to go through a more difficult installation procedure. See 
[here](https://www.psycopg.org/psycopg3/docs/basic/install.html) for installation instructions.



# Running Postgres Locally Using Docker Compose

In the corresponding [github repo](TODO), you will find a docker compose file, that contains the necessary definitions
to run Postgres locally. 

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    restart: always
    shm_size: 128mb
    ports:
      - 5432:5432
    volumes:
      - ./data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=secret
      - POSTGRES_USER=admin
      - POSTGRES_DB=mathbyte
```
This basically will run Postgres 16 (latest version of 16.x), set up a local folder
mapping from `./data` to the container's Postgres data folder, map port `5432` in the
container to port `5432` on your host, and define the Postgres database, user and password.

(This is probably not how you want to do things in production, but for local dev this
approach is perfectly fine.)

To run Postgres you should type this in your terminal:

```bash
docker compose up -d
```

If all goes well, you should see a message that the container has started.

You can also check the status of your containers using:
```bash
docker compose ls
```

And to view the logs you can run:
```bash
docker compose logs -f postgres
```

Use `Ctrl+C` to exit when you no longer want to follow the Postgres logs.


## Using YoYo Migrations

A migration is simply a series of commands to alter the database. Each migration defines some 
DDL (data definition language) commands to do things like create tables, define indexes, or even DML (data manipulation
language) commands to insert/update/delete data in various tables.

When we use YoYo, we "apply" a migration. This will essentially run our DDL/DML commands against the SQL database.

We make changes to our database over time by creating new migrations. YoYo keeps track of what migration has already 
been applied to the database, and will only run the ones needed. Normally, we also define a rollback mechanism
when creating a migration, that will allow YoYo to undo the changes made by one or more migrations.

For example, a migration may define a `create table` command. The corresponding rollback would be a `drop table`
command.

These migrations are simply files in our project, and hence can be included in our git repo - that way, we have our
entire database structure defined using code, and we have version control too, both with YoYo migrations, as well 
as git.

To use YoYo, we first have to configure it so it knows which Postgres server to talk to, what database, and the 
connection settings - again the way I do things here are fine for local dev, but not for production where you would
certainly not want your database credentials included as part of your repo.

Although you can specify these settings directly on the command line, here I am going to set up a `yoyo.ini` file
in the root of our project.

```ini
[DEFAULT]
sources = %(here)s/migrations
database = postgresql+psycopg://admin:secret@localhost/mathbyte?port=5432
verbosity = 2
batch_mode = on
```

We can now start creating one or more migrations that YoYo can apply (or rollback) in order.

In this repo, you will find a folder named `migrations` - that's where we are going to save our migrations. 

To create our first migration (remember our database is currently empty), we run this command:

```bash
yoyo new -m "db init"
```

When we do this, you'll see a new file has been created in the `migrations` folder, ending with the name `db-init`
which was based on the `-m` argument we provided when we ran the command.

Time to edit this file and create our first migration.

Let's look at it:
```python
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
        """
        DROP TABLE employee;
        """
    )
]
```

A migration can contain multiple steps - in this case just a single step, but we could add more if we wanted to.

A step has at least one argument, a SQL statement to "execute" when applying (or rolling "forward") the migration, and,
optionally, though I personally don't consider it optional, a statement to "undo", or "rollback" the migration.

In this case, we create a table called `employee`, and the rollback drops that table.

Now, we can ask YoYo to give us a list of all our migrations:

```bash
yoyo list
```

You should see something like this in the output:

```text
STATUS    ID                         SOURCE
--------  -------------------------  ------------------------------------------------
U         20240604_01_u0XKn-db-init  /Users/fbaptiste/dev/scratch/postgres/migrations
```

We can see we have one migration, and it's status is `U`, which means **unapplied**.

To apply the migration (in this case just one), we run this command:

```bash
yoyo apply
```

Now this has done several things. If you check the database, you'll see that our `employee` table has been created,
along with several tables used by YoYo internally to keep track of the status of the database compared to the migrations
define in our `migrations` directory.

We can run `yoyo list` again, and this time you should see:
```text
STATUS    ID                         SOURCE
--------  -------------------------  ------------------------------------------------
A         20240604_01_u0XKn-db-init  /Users/fbaptiste/dev/scratch/postgres/migrations
```

The `A` here, means the migration has been applied.

We can rollback the migration, by issuing this command:

```bash
yoyo rollback
```

This used our rollback code (the table drop statement), and we end up with a database that no longer
contains the `employee` table, and `yoyo list` once again shows us that our single migration is no unapplied (`U`).

Let's re-apply the migration: `yoyo apply`


Ok, so now, let's write a second migration. Suppose we realize later that we want to name that table `employees`,
not `employee`. To do that, we just need to change the table name (remember, once a migration has been defined and 
applied to your production database, it is essentially set in stone, we cannot go back and modify it - instead we 
have to use a new migration each time to define new entities or modify our database structure).

So, let's create a second migration:
```bash
yoyo new -m "rename employee table"
```

Once again, a new migration file is created, and we edit it this way:

```python
steps = [
    step(
        "ALTER TABLE employee RENAME TO employees;",
        "ALTER TABLE employees RENAME TO employee;",
    ),
]
```
Our step has both a roll forward (renames `employee` to `employees`) and a roll back statement (renames `employees`
back to `employee`).

Once again, we can apply this migration: `yoyo apply`. And if you check `yoyo list` you'll see that both migrations
have now in effect (`A`), and the database `employee` table has been renamed to `employees`.

Now, we can rollback this migration (a single one at a time)

```bash
yoyo rollback 
```

Or, we can rollback to a specific revision (the revision number is in the migration file). To try this out,
let's re-apply the migration (`yoyo apply`), and roll back everything up to and including the first migration 
(or revision):

```bash
yoyo rollback  -r 20240604_01_u0XKn-db-init
```

If you check `yoyo list` you'll see that both our migrations have been rolled back (and our `employee` table is 
gone from the database).

To have yoyo apply all the migrations, simply run `yoyo apply` and all migrations will be applied.


Ok, let's do one last migration - a more complicated one this time.
Let's say that after a while we decide we don't want the `department` field to be freeform text. Instead,
we want to create a new table (named `departments`) that will have all the departments, with some ID, and 
our `employees` table should reference the department ID instead (as a foreign key).

How would we go about doing that?

- create a `departments` table
- populate that table based on all the values available in `employees.department`
- add a new column to `employees` called `department_id`
- populate `department_id` with the appropriate department id as defined in the `departments` table
- set up a foreign key relationship from `employees.department_id` to `departments.id`.


Before we do that, I'm going to create a new migration to insert some test data in our `employees` table - that's 
probably not how you would do this in practice, but I haven't shown you how to use Python and `psycopg` yet, so 
let's hack things a bit. 

Create a new migration `yoyo new -m "generate sample employee data"`, and specify some data to insert into the table.
As usual, I also specify the rollback command (which basically deletes all rows from the `employees` table).

Now, that we have some test data, let's go ahead with our plan.

```bash
yoyo new -m "change departments to FK"
```

Once you have created all the steps (and their corresponding rollbacks), you can now apply this latest migration
using `yoyo apply`. Of course, you can also roll it back, and even rollback all the migrations currently applied to 
the database using:

```bash
yoyo rollback -a
```

Ok, so this was some of the functionality provided by YoYo, and will probably cover most of what you are likely to need.

However, YoYo has a lot more functionality, so if you find this database migration tool of interest, check out
the docs or some web searches for more info.

There are alternatives to YoYo - `alembic` is a pretty popular one, mainly because it integrates with SQLAlchemy, and
whenever you make changes to your ORM models, alembic can automatically pick up on the changes and generate migrations 
for you (though in my experience you often have to "fix" the migration manually). Alembic has a ton of extra 
functionality and extensibility, especially when tied with SqlAlchemy, but again, it's a lot to learn. I already know
the SQL syntax, and find YoYo to be the perfect match for a lazy developer like me! 


## Using Python and psycopg to Interact with the Postgres Database

Next, we look at how we can use `psycopg` to access our database in Python code.

The first we'll need to do is to establish a connection. For local development a simple connection is probably 
sufficient, but for larger production systems (especially when dealing with APIs that can potentially try to have 
multiple open connections at the same time), then we should use a connection pool - but for the
simple examples here, I'll just stick to regular connections.

Again, since this is local dev, and to keep the length of this mini series somewhat sane, I'm not going to worry about 
how secrets are stored - needless to say, in an actual development environment what I'm doing here (storing secrets 
right in the code) is a **huge** no-no. See some of my previous videos on how you can set up your projects to use 
environment variables for a better (but not the only) solution. In practice I often use a combination of environment 
variables and/or secrets stored in AWS Secrets Manager.

Once we have our connection pool established, we'll use plain SQL statements to query our database, as well as insert
or delete data. I'm not going to get too much in-depth with the `psycopg` library - my main goal here is to
show you how we can use the concept or **row factories** in `psycopg` to load data from our database tables
directly into Python objects (tuples, dictionaries, data classes, and Pydantic models).

Let me know in the comments if you would like more videos on SQL 

## Conclusion
So, we have seen how to set up Postgres using Docker, use code for version control of our database structure (and even
contents), and how to leverage row factories in `psycopg` to load SQL data directly into Python objects.

And all this without having to learn any ORM. Of course, this does mean that you need to have some basic knowledge
of SQL. But keep in mind that if you are aiming to be a data analyst, you will likely need to learn SQL at some point
anyway - even if you only ever work with No-SQL databases, many of them often use some "flavor" of SQL 
(e.g. ClickHouse, Couchbase, Cassandra, etc)

Basic SQL is not difficult, and that basic SQL can probably account for 80% of the functionality you will need. The 
rest is often specific to the database platform you are using, involving things such as various ways
of handling more complex data types (arrays, maps, dates and times, etc), or even extensions sucn as `timescaledb`
for Postgres, and a whole variety of other things.

Let me know in the comments if there are specific parts of SQL or Postgres you would like me to cover in the future, 
(things like primary keys, foreign keys, indexes, join types, CTEs, aggregation, etc), or how to use `psycopg` 
(such as avoiding SQL injection attacks, etc).

