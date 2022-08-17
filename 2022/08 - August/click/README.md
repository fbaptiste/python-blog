# Using `click` to build a Python command line tool

In this example, we're going to look at how to use the `click`
library to build a Python based command line interface (CLI).

Sure, you could use the `argparse` standard library module, but if
you've worked with `argparse` before, or seen my video on it in my 
[Python deep dive course](https://www.udemy.com/course/python-3-deep-dive-part-1/?referralCode=E46B931C71EE01845062),
you'll know that using `argparse` can be a lot of hard work.

Instead, `click` is going to make this a breeze!

> **Note**: Consider this directory as a stand-alone project - i.e. do 
> not try to run directly from the main blog repo root. Instead, make 
> a separate project out of it.
 
## Installing
The documentation for the `click` library is located [here](https://click.palletsprojects.com/).

The bulk of the documentation for what we'll cover in this video can be 
found [here](https://click.palletsprojects.com/en/8.1.x/#documentation)


You will need to create a virtual environment and install `click` using `pip`:
```bash
pip install click
```

We'll also use a few more libraries for this project (which you'll also need to install - checkout the `Pipfile` 
or `requirements.txt` for exact details):
 
- `setuptools`
- `tabulate`

Optionally:
- `isort`
- `black`

I use these code formatters to standardize my Python code (I also use linters such as `flake8`, but I'm not going to 
get into that in this video - I'll do a dedicated video on `flake8` in the future.)

You'll find a `Makefile` included with this project that you can use for more easily running `black` and `isort` - 
assuming you are on Mac/Linux.

For more details on `black` and `isort` check out 
my [Youtube channel](https://www.youtube.com/channel/UCOsGw17tMhM4-GBjvQnXGzQ) - there is a video on the subject there.



## A Simple Start

> code is in `main.py`

We start with a very basic example of how to create a CLI with the commands `time` and `date` that should
print out the current (UTC) time and date.

This example also shows us how we can request the auto generated `--help` docs for your CLI - not much there right now,
but at least it shows us the available commands in our CLI:

```bash
python main.py --help
```

We can then call the `date` or `time` commands this way:
```bash
python main.py date
```

```bash
python main.py time
```

So this works, but having to type `python main.py` every time is going to quickly become very tedious indeed.


## Using `setuptools`
So... we're going to use `setuptools` - I'm not going to get into the details of `setuptools` here - I'll just show 
you how to use it specifically to set up our CLI in a more convenient manner.

Docs for `setuptools` are located [here](https://setuptools.pypa.io/en/latest/).

If you have not already installed `setuptools` in your environment, install that library now:

```bash
pip install setuptools
```

Next we are going to create a `setup.py` file, that will basically define an **entry point** to our CLI. And we can 
also give our CLI a name - for this example I'll simply use `cli` as our name, and it will basically "point" to
our `main_cli` function in `main.py` as the **entry point**.

We place this `setup.py` file in our project root.

Once we have that file created, we'll install the package it defines using `setuptools`.

We're also going to use the `--editable` flag. Doing so enables the functionality that whenever we change our CLI 
code, those changes are automatically reflected in the CLI without having to re-install the package (otherwise we 
would have to re-install the package every time we make a change in our code - much more convenient for development).

Also, before running our setup go ahead and remove (or comment out) the entire section:
```python

if __name__ == '__main__':
    main_cli()
```

Now, from your project root, go ahead and run this command:
```bash
pip install --editable .
```
(don't forget the period (`.`) at the end of that command!)

Once that has been successfully installed, you can invoke our CLI by simply typing `cli` on the command line, e.g.

```bash
cli --help
```
or
```bash
cli date
```

You can always uninstall your CLI, by running:
```bash
pip uninstall my-super-duper-cli
```

## Main CLI

Let's now write our main CLI, and explore some of the options `click` provides us to build
up a more complex CLI.

Here's the basic functionality we want our CLI to have:
- a CSV previewer
  - for all lines in the CSV file
  - the first N rows
  - all nicely formatted (we'll use  the `tabulate` library to help us there - 
    check my [YouTube channel](https://www.youtube.com/channel/UCOsGw17tMhM4-GBjvQnXGzQ) for a video on the `tabulate` library)
- a JSON previewer:
  - entire file
  - first N "lines"
  - also nicely formatted
- a converter to convert a CSV file to a JSON representation
  - If the CSV file contains a header row we'll have the option to use that
  - or, we'll have the option to manually specify the column headers ourselves in the CLI (useful for providing headers
    if the CSV file does not contain a header row, or if we want to override the header row)
  - for simplicity, we're going to ignore data types in the CSV file, and assume every field is a string
 
### Step 1
First, you'll need to install the `tabulate` library if you have not already done so - you can find 
it [here](https://github.com/astanin/python-tabulate)

```bash
pip install tabulate
```

### Step 2
We're going to split our code, and our CLI, over multiple modules, just like you would in a real project.

We'll start by creating:
- a package `viewers` with these modules:
  - `csv_viewer.py`: this will contain our code for our CSV previewer
  - `json_viewer.py`: this will contain our code for our JSON previewer
  - `__init__.py`: we'll use this to define the CLI command group and commands
- a package `converters` with these modules:
  - `csv_converter.py`: this will contain our code for converting a CSV file to a JSON file
  - `cli.py`: we'll use this module to define the CLI command group and commands


### Step 3
We'll start by creating two command groups in our CLI:
- a `viewers` command group to group our viewer commands together, e.g. we'll be able to call
  our viewers with syntax like:

  ```bash
  cli viewers csv <file_name> + options 
  cli viewers json <file_name> + options
  ```
- a `converters` command group for our converters (we'll only have one for this example), call syntax like
  ```bash
  cli converters csv <file_name> + options
  ```
 
We'll create the `converters` group in the `cli.py` module - you could implement it directly in the 
`csv_converter.py` file, or create a regular package with an `__init__.py` and implement it there, or 
you could implement it in any other module in the project for that matter. This is just a choice I am making to show 
you how flexible `click` is when building up your command line - you can really do this however you want.

For the `viewers` group, I'll use the `viewers` `__init__.py` file to create the command group and commands.

### Step 4
Once we have our two command groups created, we'll need to add them to the main CLI in the `main.py` file.

To do that, we simply import the groups (the decorated functions we just created), and add them
as commands to our root CLI group in `main.py`.

### Step 5
Let's implement the code to view the CSV files - no command line, yet, just the basic code.

I'll use the csv file, `data/population.csv`, containing total population by country, which I found
[here](https://data.worldbank.org/indicator/SP.POP.TOTL).


### Step 6
Implement the JSON viewer - again just as a plain function in our module.

### Step 7
Implement the CSV to JSON converter - again just the code that does the actual work.


> You'll notice that the code we have written so far, is just plain Python. We can use it in a larger application
> just like any module we write. The difference is that we are **also** going to add CLI layers on top of our 
> existing Python code - the CLI is basically just another way to
> invoke the functionality we want to expose via a command line. 
> 
> Some people try to use a mixture of `if __name__ == '__main__'` in different modules all over the place, but then
> get tripped up because the imports can start failing because the root changes depending on what module you use as 
> your "start" module- instead expose functionality via a CLI, much more robust!


### Step 8
Now we'll start implementing the CLI.

We'll start by just stubbing out the various commands, in the `viewers/__init__.py` and
`converters/cli.py` files.

Test the CLI out now by running these commands:
```bash
cli --help
cli viewers --help
cli converters --help
```


### Step 9
Now let's implement the CLI for the JSON viewer.

We have a few things we'll want to do:
- option to specify the JSON file we want to view (there's a sample one the `data/` folder)
- option to view the entire file or the first N lines
- option to specify the indentation we want for our JSON
- some help text to explain what the command does, as well as documenting the parameters

For example, we'll want the ability to issue the command in these ways:

- `cli viewers json data/sample.json`: views the entire file specified, with a default indent of `4` spaces (which 
  you'll note is different from the `preview_json` function which itself defaults the indent to `2`)
- `cli viewers json -n 10 data/sample.json` or `cli viewers json --numlines 10 data/sample.json`: views the first `10` lines
- `cli viewers json -n 10 -i 3 data/sample.json` or `cli viewers json -n 10 --indent 3 data/sample.json`: sets the 
  indent to `3`
- `cli viewers json --help`: should display some help about the command and its parameters

So, basically we want to specify the file without having to use a flag (so like a positional argument, and termed 
an **argument** in `click` terminology), and have two flags `-n` (or `--numlines`) for number of lines (not set means 
the entire file), and `-i` (or `--indent`) to specify the indentation, with a default of `4` if not set (these are 
called **options** in `click` terminology). 

For both of these options we'll want to validate that the values are integers are in the proper range (we'll use a `None` 
value for `--numlines` to indicate no limit, so we should validate this value as `None` or `> 0`, and for `--indent` we'll 
want to validate the value `> 0`.) 


### Step 10
Implement the CSV viewer CLI.

This one has a few more options:
- a positional argument for the file_name
- `--numlines`/`-n`: first n lines of the CSV file, defaults to `None` (entire file)
- `--has-header`: a flag (with no value) to indicate whether CSV file has a header row or not
- `--format`/`-f`: one of several possible values to indicate the table formatting style - default to `fancy_outline`.



### Step 11
Implement the CSV to JSON converter CLI

For this one we'll use the following options and skip arguments altogether:
- an input file
- an output file
- flag to indicate if CSV file has headers
- an option to specify custom column headers (in practice this could be tedious for large 
  numbers of columns, but serves well as an example of a multivalued option)

