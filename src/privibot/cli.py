"""
Module that contains the command line application.

Why does this file exist, and why not put this in __main__?

You might be tempted to import things from __main__ later,
but that will cause problems: the code will get executed twice:

- When you run `python -m privibot` python will execute
  ``__main__.py`` as a script. That means there won't be any
  ``privibot.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``privibot.__main__`` in ``sys.modules``.

Also see http://click.pocoo.org/5/setuptools/#setuptools-integration.
"""

import logging
import os
import sys

from telegram.ext import CommandHandler, Updater

from . import callbacks


def main():
    """The main function, which is executed when you type ``privibot`` or ``python -m privibot``."""
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

    token = os.environ.get("TELEGRAM_BOT_TOKEN")

    if not token:
        print("You must set the bot token in the environment variable TELEGRAM_BOT_TOKEN\n", file=sys.stderr)
        return 1

    updater = Updater(token=os.environ.get("TELEGRAM_BOT_TOKEN"), use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", callbacks.start))
    updater.dispatcher.add_handler(CommandHandler("help", callbacks.help))
    updater.dispatcher.add_handler(CommandHandler("myPrivileges", callbacks.my_privileges))
    updater.dispatcher.add_handler(CommandHandler("requestAccess", callbacks.request_access))
    updater.dispatcher.add_handler(CommandHandler("grant", callbacks.grant, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler("revoke", callbacks.revoke, pass_args=True))

    logging.info("Starting Bot")
    updater.start_polling()

    logging.info("Putting Bot in idle mode")
    updater.idle()

    return 0
