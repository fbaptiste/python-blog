"""Example 12

In this example we are going to see how to use the logger hierarchy. This example will use one logger
per module in some parts of our application, and also use less granular loggers for other part,
leveraging the fact that loggers are singleton objects.

There is one major kind of issue we need to contend with. The problem is that logging was probably
not designed to use global variables for getting the logger instances.
When you get a logger (getLogger(name)), it will create that logger if it does not exist.

If you use a global variable in your module to get and store a ref to the logger for that module (so that you can
then use it in various classes and functions in that module without having to call getLogger(name) inside every
function you implement), then be aware that the logger is created immediately upon import.

The problem is if this import happens **before** you configure the logging system.
The way logging is implemented, when you run the configuration for your loging system, it will run through each
existing logger and disable any existing loggers not defined in your config (unless you explicitly set the
disable_existing_loggers setting to False in the config file - it defaults to True.)
I will show you this in the code.

So, if disable_existing_loggers is set to True (or not set since default is True), **and** you create loggers
in your code **before** the configuration happens, those loggers will be disabled and won't work as expected.

So, the moral of the story is that you need to make sure you do not run getLogger(name) before you configure
the logging system, or just set disable_existing_loggers to False.

Here I chose to set disable_existing_loggers to False.
"""

import logging
from datetime import datetime

from configs import log_config
from services import aws, azure, gcp
from utils import formatters

if __name__ == "__main__":
    print("*** Running log configuration...")
    log_config.configure_loggers()

    # Logging to my_app logger
    # Create the logger here is fine, not only is it created after configuration has happened, but it is also
    # explicitly defined in the configs
    logger = logging.getLogger("my_app")
    logger.info("This is a test message from the main module")

    # Will log to services.aws, services.azure and services.gcp loggers
    # Those loggers are not explicitly defined in the configs
    aws.list_s3_bucket("aws_bucket")
    azure.get_sql_server_connection()
    gcp.upload_file("source", "target")

    # Will log to utils logger
    # That logger is explicitly defined in the configs
    formatters.format_date_standard(datetime.now())
