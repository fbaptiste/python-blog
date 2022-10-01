# The `flake8` Library

## Introduction
> Note: Please treat this as an independent project - it has its own `requirements.txt` file (for `pip` installing), 
> and a corresponding `Pipfile` (for `pipenv` installations).

`flake8` is a tool for Python style enforcements according to conventions generally agreed upon by Python developers
worldwide. But it is also more than just style - it can help you find bugs in your code, possible security issues, bad
design, etc.

We're going to add `flake8` to our existing `black` and `isort` tools that I covered in a previous video.

The `flake8` system has a base system, and a whole slew of extensions, or **plugins** using its terminology, that 
extend the checks that `flake8` can perform.

When you run `flake8` against your code, any "violation" is reported using a code- these are generally numbers with 
a letter prefix such as `F401`, `E201`, etc. In general every plugin (built-in, or added) has it's own, unique, 
character prefix (sometimes more than one character). 

The documentation for `flake8` can be found [here](https://flake8.pycqa.org/en/latest/#).

## Plugins
By default, `flake8` includes the `pycodestyle`, `pyflakes` and `mccabe` checkers:
- [pycodestyle](https://pycodestyle.pycqa.org/en/latest/) - largely style (pep8) related
- [pyflakes](https://github.com/PyCQA/pyflakes) - things like unused imports, duplicate function args, etc
- [mccabe](https://github.com/pycqa/mccabe) - a measure of code complexity

You can read more about the McCabe cyclomatic complexity [here](https://en.wikipedia.org/wiki/Cyclomatic_complexity) - 
it can be a tough read, but basically think of it as something that will warn you if your code is too complex 
(not necessarily hard to read, just too much complexity, usually caused by too many levels of nesting)

We're also going to add a few plugins, the ones that I typically use on all my Python projects - feel free to change
it up as fits your needs - but really ask yourself **why** you would **not** want to perform these checks! I'm not
saying you absolutely have to, I'm saying think about why you would want or not want certain checks in place - and 
this may very well vary from project to project.


- [bugbear](https://github.com/PyCQA/flake8-bugbear): can find a variety of bugs and design problems
- [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions): helps improve your comprehension code
- [flake8-implicit-str-concat](https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat): this one helps 
  with implicit string concatenation - I use mainly because `black` can introduce some weirdness when reformatting a
  string literal that was written over several lines, but would actually fit on a single line, e.g.
  ```python
    a = (
        "this is a string literal "
        "that would fit on a single line"
    )
    ```
    will be changed to:
    ```python
    a = "this is a string literal " "that would fit on a single line"
    ```
    This `flake8` extension will identify those kinds of issues that may arise after running `black`.

- [pep8-naming](https://github.com/PyCQA/pep8-naming): Checks pep8 naming conventions
- [flake8-builtins](https://pypi.org/project/flake8-builtins/): Makes sure you don't accidentally use a Python builtin 
  for variable or parameter names
- [flake8-bandit](https://github.com/tylerwince/flake8-bandit): Runs the `bandit` tool set against your Python 
  code - more info on `bandit` is [here](https://bandit.readthedocs.io/en/latest/). This toolset can identify common
  security issues in your Python code.
- [flake8-eradicate](https://github.com/wemake-services/flake8-eradicate): warns you of any commented code - for larger
  code projects, you should be using some source control system, such as git - you do not need to comment code out, 
  instead delete it and use version control to retain the history of your code.
- [flake8-print](https://github.com/jbkahn/flake8-print): checks for print statements in your code (production code
  usually should not contain print statements)

## Violation Codes
Here you'll find links to pages that list and describe the various violation codes, both for `flake` itself, as 
well as the additional plugins we're using.
- `flake8` pre-installed:
  - `pycodestyle` - Exxx, Wxxx
  - `pyflakes` - Fxxx
  - `mccabe` - C901
  - [codes list](https://www.flake8rules.com/) 

- `flake8-builtins`:
  - `Axxx`
  - No formal docs for these codes, but from the 
    [source](https://github.com/gforcada/flake8-builtins/blob/master/flake8_builtins.py) we see there are 
    only three codes:
    - `A001` (variable shadows a built-in)
    - `A002` (callable parameter name shadows a built-in)
    - `A003` (class attribute shadows a built-in)
- `flake8-bugbear`:
  - `Bxxx`
  - [codes list](https://github.com/PyCQA/flake8-bugbear)
- `flake8-comprehensions`
  - `Cxxx` (except C901, McCabe complexity which is reported by `flake8` itself)
  - [codes list](https://github.com/adamchainz/flake8-comprehensions)
- `flake8-eradicate`
  - only one: `E800` (found commented code)
  - [codes list](https://github.com/wemake-services/flake8-eradicate)
- `flake8-implicit-str-concat`
  - `ISCxxx`
  - [codes list](https://github.com/flake8-implicit-str-concat/flake8-implicit-str-concat)
- `flake8-naming`
  - `Nxxx`
  - [codes list](https://github.com/PyCQA/pep8-naming)
- `flake8-bandit`
  - `Sxxx`
  - Technically bandit uses codes in the range `Bxxx`, but since that code is already taken by bugbear, it is
    remapped to `Sxxx`
  - [codes list](https://bandit.readthedocs.io/en/latest/plugins/index.html#complete-test-plugin-listing)
- `flake8-print`
  - `Txxx`
  - [codes list](https://github.com/jbkahn/flake8-print)


## Other Plugins
There are many articles and blog posts around people's favorite `flake8` extensions - just do some web searches
and you're bound to find some.

This particular repo 
([https://github.com/DmytroLitvinov/awesome-flake8-extensions](https://github.com/DmytroLitvinov/awesome-flake8-extensions))
has a fairly comprehensive list - but before you decide to use one of the extensions, just make sure they are
(a) relatively popular, and (b) are still actively being developed.


## Installation and Configuration
To install everything for this video we'll pip install the following:
```bash
pip install flake8
pip install flake8-bugbear
pip install flake8-comprehensions
pip install flake8-implicit-str-concat
pip install pep8-naming
pip install flake8-builtins
pip install flake8-bandit
pip install flake8-eradicate
pip install flake8-print
```

We'll create the same configuration as before for `black` and `isort`, in the `pyproject.toml` file.

(I'm setting my line length to 80 to ensure I have code formatted to a shorter line length as I have to make the font
larger for the videos, feel free to set it to whatever you want.)


We can also configure `flake8`, but it will not work with our `pyproject.toml` file, so we'll create a file 
named `.flake8` which will contain the configs for flake.

I'll explain what I have in my `.flake8` config file in the video, as these are the most common config options, but 
there are many more configuration options available, 
documented [here](https://flake8.pycqa.org/en/latest/user/configuration.html) and 
[here](https://flake8.pycqa.org/en/latest/user/options.html#options-list).


## Running `flake8`
In this repo you will find a Python file (called `bad_code.py`, and a copy of it in `bad_code_original.py`) that 
contains a slew of issues - the code works, but the style is terrible, and should be refactored - `black`, `isort` 
and `flake8` will help us get there.

To run `flake8` on all your files simply run this from the command line:
```bash
flake8 
```

You can target specific files also:
```bash
flake8 ./bad_code.py
```

(You can also specify multiple files, or even paths if you prefer.)


### Steps

1. Let's start by running `flake8` just to get an idea of what's wrong: `flake8 bad_code.py`
2. Now let's use black and isort to clean things up:
    1. `black ./bad_code.py`
    2. `isort ./bad_code.py`

3. That eliminated quite a few linter issues, but now we have to do the rest by hand - just tackle one at a time.

> Note: When refactoring code that is already in "production", best practice is to ensure you have full unit 
> test coverage for all the code you are refactoring - that way, you can refactor and be (fairly) certain your changes
> did not break the existing functionality. How would you know otherwise? :-)
