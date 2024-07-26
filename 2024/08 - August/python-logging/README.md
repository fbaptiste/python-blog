# Demystifying Python Logging - Coding

This is a follow up to my previous post Demystifying Python logging - Concepts. 
If you have not watched it, and are not already familiar with Python logging concepts such as log records, levels, 
loggers and logger trees, handlers, formatters, filters, etc, I recommend that you watch that video first.

This video is going to be a hands-on coding session where we'll explore all these topics.

## Useful Links and Info
The following are useful links and information that we'll sometimes refer to in this video:
- Python logging documentation: https://docs.python.org/3/library/logging.html
- Logging levels: https://docs.python.org/3/library/logging.html#logging-levels
- LogRecord attributes: https://docs.python.org/3/library/logging.html#logrecord-attributes
- Built-in Handlers: https://docs.python.org/3/library/logging.handlers.html

## Examples
We are going to work through a variety of examples in this video:

1. Example 1: Creating the root logger, inspecting a logger to determine some of its properties
2. Example 2: Creating the main application logger with a YAML file configuration
3. Example 3: Using code instead of a YAML file to configure the logger
4. Example 4: Setting up a FileHandler
5. Example 5: Setting up a RotatingFileHandler
6. Example 6: Setting up multiple Handlers
7. Example 7: Customizing the String Formatter
8. Example 8: Using the extra Parameter
9. Example 9: Creating Custom Filters
10. Example 10: Creating Custom Formatters
11. Example 11: Suppressing Logging Exceptions for Production
12. Example 12: Setting up and using Multiple Loggers


## Conclusion
As you will have seen from these examples and my last video, conceptually, Python logging is not complicated.

What can make things complex is the flexibility offered by the logging system, which combined with rather poor
documentation, can make it difficult to sometimes understand what is going on with your logs.

For this reason, I recommend that you always start simple, and only add complexity as you need it.

There is also an additional way to configure your logging, which is to use the `basicConfig()` function. This is 
basically trying to simplify the dict configuration method, and is simpler than the code based setup I showed you.
However, it is not introducing any new functionality, so I don't cover it here. If you understand the code
we have discussed in this video, you'll understand exactly how to use `basicConfig`.

Alternatively, you have 3rd party logging libraries that are more modern and easier to use, such as structlog, 
loguru, etc. However, I recommend that you first understand the Python logging module, as it is part of the
standard library and you will likely encounter it in many projects. Many of the concepts in these 3rd party logging 
libraries are similar to those of the standard library logging module, and in fact can often integrate directly with it.
