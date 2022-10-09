# The `python-dotenv` Library

## Installation and Documentation
The project can be found [here](https://github.com/theskumar/python-dotenv).

You will need to pip install `python-dotenv` to use this library

## For those using `pipenv`
If you use `pipenv`, that system already supports using a `.env` file to automatically load environment 
variables defined in a `.env` file when the virtual environment is activated. However, not everyone 
uses `pipenv` for their virtual environments, and this is where `python-dotenv` comes in useful.

For this demo I am therefore **not** going to use `pipenv`, but instead use Python's built-in virtual environments:
```bash
python3.10 -m venv .venv
```
Then activate the environment:
```bash
source .venv/bin/activate
```
And finally install the library:
```bash
pip install -r requirements.txt
```

We can check that the library was installed:
```bash
pip freeze | grep dot
```

## Overview
Often we use environment variables when our Python applications are deployed to production 
systems to configure a variety of settings used by our apps.

Typically various mechanisms are used in CI/CD pipelines to populate those environment variables.

When we are running the system locally however, we need to make sure that these environment variables 
exist prior to us running the app. Certain IDEs allow you to configure those environment variables,
or you could use some other mechanism (such as a Makefile, or specifying the env variables on the command line
that runs your Python app), but a simpler way is to use the `python-dotenv` library.

This library basically "injects" environment variables defined in a `.env` file in your project root.

The advantage of using a file to store the environment variables is that it is easy to add to `git` (or other 
versioning system), although if certain secrets (such as API keys) are defined in your `.env` file you may not want 
to include those in the repo.

Typically the way I approach this is to create two files:

- `env-template`: a file that has the basic environment variables, but omits any sensitive values, for example:
    ```txt
    SWAPI_BASE_URL=https://swapi.dev/api
    SECRET_1=
    SECRET_2=
    ```
- `.env`: a file that has all the environment variables populated, including the secrets, for example:
    ```txt
    SWAPI_BASE_URL=https://swapi.dev/api
    SECRET_1=secret_value_1
    SECRET_2=secret_value_2
    ``` 

I then **include** `env_template` in the git repo, but **exclude** (aka **ignore**) the `.env` file. That way I can
let other people know what the `.env` file should look like, but I do not run the risk of accidentally including
my `.env` file with secrets populated. (For this demo I am including the `.env` file in the repo, but in practice 
I do not).

Once we have this in place, we can use `python-dotenv` to "inject" the environment variables from the `.env` file, 
and access them in Python the usual way (`os.getenv`), for example:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # this "injects" the environment variables located in .env

swapi_base_url = os.getenv('SWAPI_BASE_URL')
secret_1 = os.getenv('SECRET_1')
secret_2 = os.getenv('SECRET_2')
```

One thing to note is that we now have several ways to define environment variables:
- in the `.env` file
- as regular environment variables in our terminal session
- as command line arguments, e.g.
  ```bash
  SWAPI_BASE_URL=https://swapi.dev/api SECRET_1=100 SECRET_2=200 python main.py
  ```

What happens when we mix these different ways of defining env vars?

The command line version overrides any pre-existing standard environment variable (so if you have an env var
defined in your terminal session, the command line definition will override it).

Any value in `.env` will be **overridden** by a standard env var definition, and in turn will be overridden
by the command line definition.

So the **priority order** in which environment variables are picked up is:
1. command line argument
2. session environment variable
3. `.env` file.


For example, if you have this scenario:
- `MY_VAR_1=100` in your terminal session
- `MY_VAR_1=200` in your `.env` file
then once you load `.env` using `load_dotenv()`, the value of the env var `MY_VAR_1` will be `100`.

And if you have this:
- `MY_VAR_1=100` in your terminal session
- `MY_VAR_1=200` in your `.env` file
- run your script using `MY_VAR_1=300 python myscript.py`
then once you load `.env` using `load_dotenv()`, the value of the env var `MY_VAR_1` will be `300`. 


## More Advanced Features
There are few more tricks up `python-dotenv`'s sleeve. One very useful one in particular is the ability
for it to do variable interpolation.

For example, we could define an `.env` file this way:
```text
BASE_URL=https://swapi.dev/api
FILMS_URL=${BASE_URL}/films
```

When the `.env` file is loaded, `FILMS_URL` will actually be `https://swapi.dev/api/films`

## Trying it out
To try all this out, we'll run `main.py` in different ways.

First, let's make sure those environment variables are not defined in our session:
```bash
env | grep 'SECRET\|SWAPI'
```

First, we'll run `main.py` "normally":
```bash
python main.py
```

Notice the results:
```text
SWAPI_BASE_URL:  https://swapi.dev/api
SWAPI_FILMS:  https://swapi.dev/api/films
SECRET_1:  100
SECRET_2:  200
```

Also notice that the environment variables are still not defined in our session.


Next, we are going to set `SECRET_1` to some specific value in our current terminal session:
```bash
export SECRET_1=abcdefg
```
and let's check that the variable is set in our session:
```bash
env | grep 'SECRET\|SWAPI'
```

If we run 
```bash
python main.py
```

we get this output:
```text
SWAPI_BASE_URL:  https://swapi.dev/api
SWAPI_FILMS:  https://swapi.dev/api/films
SECRET_1:  abcdefg
SECRET_2:  200
```

You'll notice that `SECRET_1` is set to the value we defined in our session environment variable.

Finally, with that session variable set, let's override it using a command line arg when we run our script:
```bash
SECRET_1=tuvwxyz python main.py
```

We get this output:
```text
SWAPI_BASE_URL:  https://swapi.dev/api
SWAPI_FILMS:  https://swapi.dev/api/films
SECRET_1:  tuvwxyz
SECRET_2:  200
```

and you'll notice that `SECRET_1` now has the value we specified on the command line.
