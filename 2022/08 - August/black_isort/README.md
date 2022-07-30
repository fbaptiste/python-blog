# Python `black` and `isort`

`black` and `isort` are code formatters that will modify your Python code to conform to (PEP8) standards.

By using tools like `black` and `isort`, development teams ensure a common style for their Python code.

`black` looks at things like indentation, line length, use of double quote for strings, trailing commas in multi-line lists/tuples/dicts, and much more.

`isort` is primarily focused on the location and order of **imports** in your modules. It will automatically sort your imports alphabetically, as well as split up your imports into sections, normally for standard library, 3rd party libraries, and your own project's modules/packages. It also does some formatting
of imports (sometimes splitting an import statement over multiple lines)

In another video, we'll take a look at the `flake8` package, and knowing how to use `isort` and `black` before we do that will be beneficial.


> Note: Although this folder is part of the overall blog repo, you should consider it as a standalone project, i.e. treat this folder as your application root, create your virtual env for this root, etc.
> 

## `black` Installation
Home page for `black` is located [here](https://black.readthedocs.io/en/stable/).

You will need to install `black` to your virtual environment.

You can pip install it:
```bash
pip install black
``` 

Alternatively, if you are using this repo with `pipenv`, then the dependency is already included in the `Pipfile`, so you can just install it using 
```bash
pipenv install --dev
```


## `isort` Installation
Home page for `isort` is located [here](https://pycqa.github.io/isort/).

You will need to install `isort` to your virtual environment.

You can pip install it:
```bash
pip install isort
```

Alternatively, if you are using this repo with `pipenv`, then the dependency is already included in the `Pipfile`, so you can just install it using 
```bash
pipenv install --dev
```


## Running `black`
When you run `black`, by default it will **modify** your Python code files.

You can run `black` on a file, or a directory via the command line:

```bash
black <file_or_directory>
```

If you only want to see what changes `black` would make but **without** modifying your code fiels, use the `--diff` flag - in that case `black` will produce a diff of all the changes:
```bash
black --diff <file_or_directory>
```

## Running `isort`
Just like `black`, `isort` will modify your files by default.

You can run `isort` on a file, or a directory via the command line:

```bash
isort <file_or_directory>
```

If you only want to see what changes `isort` would make but **without** modifying your code fiels, use the `--diff` flag - in that case `isort` will produce a diff of all the changes:
```bash
isort --diff <file_or_directory>
```

## Configuring `black`
Since `black` is highly opiniated, it has very few configurations!

We can provide a configuration file for `black` by creating the file `pyproject.toml` - usually placed in the root of the project (this way the config will apply to every Python file in your project).

One configuration I see used often is to change the maximum allowed line length from `88` (`black`'s default, to something larger or smaller). In this example, I have set the max line length to `100` by adding this to the `pyproject.toml` file:

```toml
[tool.black]
line-length = 100
```


## Configuring `isort`
We can also configure `isort` using the same `pyproject.toml` file.

One of the things we **have** to do, is tell `isort` we are using `black`.

By default `isort` applies a style to format multi-line imports that is not compatible with `black`.

That setting can be added to the `pyproject.toml` file in a section for `isort`:
```toml
[tool.isort]
profile = "black"
```

There are more settings that you can read up on in the link I provided earlier, but usually that's pretty much all we need.

## Using a Makefile
If you are running on a *nix system, you can use GNU [make](https://www.gnu.org/software/make/manual/make.html) and a `Makefile` to make running `isort` and `black` a little simpler than typing all the commands directly.

If you are running in Windows, then I do not believe you have `make` available, and I am not aware of Windows based alternatives (not saying there aren't, just that I don't know - as I have not used Windows in years).

To run black and isort together, I have created two commands (or **rules**) in the `Makefile` - one for running with `--diff`, and one for running without (i.e. making changes to your files)

You can use run them from the command line:

```bash
make standardize-diff
```
to just do a diff, and

```bash
make standardize
```
to actually change your code files.


And that's it, you now know how to use `black` and `isort` to standardize your code. It's a good idea to do this, and most Python software developers do - it brings some consistency to your code, and will help you write better looking code.
