from datetime import datetime

import click

from converters.cli import converters_group
from viewers import viewers_group


# first create a command group - this will be the top level CLI
@click.group
def main_cli():
    pass


@click.command
def date():
    click.echo(datetime.utcnow().date().isoformat())


@click.command
def time():
    click.echo(datetime.utcnow().time().isoformat())


@click.command(name="click-docs")
def view_click_docs():
    """View the click library documentation"""

    """
        Since our decorator provides a `name` argument, the group name
          will be that, otherwise it would default to the function name
          with underscores replaced by dashes (it is customary for
          commands to use dashes to separate words, not underscores)

        If you do not wish to override the `name`, you can omit that (and the parentheses)
        from the decorator altogether e.g.

        Writing this:

        ```python
        @click.group
        def click_docs():
            pass
        ```

        would achieve the same thing as we have above.

        Writing this:

        ```python
        @click.group
        def view_click_docs():
            pass
        ```

        would result in a command group named `viewers-click-docs`
        """
    click.launch("https://click.palletsprojects.com/")


# add commands to CLI root
main_cli.add_command(date)
main_cli.add_command(time)
main_cli.add_command(view_click_docs)

# add command groups to CLI root
main_cli.add_command(viewers_group)
main_cli.add_command(converters_group)


# if you do not use setuptools, you'll need to uncomment this code,
# and invoke the CLI as explained in the README (better yet, check out the video in my YouTube
# channel - https://www.youtube.com/channel/UCOsGw17tMhM4-GBjvQnXGzQ

# if __name__ == '__main__':
#     main_cli()
