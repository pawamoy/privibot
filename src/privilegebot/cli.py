"""
Module that contains the command line application.

Why does this file exist, and why not put this in __main__?

You might be tempted to import things from __main__ later,
but that will cause problems: the code will get executed twice:

- When you run `python -m privilegebot` python will execute
  ``__main__.py`` as a script. That means there won't be any
  ``privilegebot.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``privilegebot.__main__`` in ``sys.modules``.

Also see http://click.pocoo.org/5/setuptools/#setuptools-integration.
"""

import os
import logging

from telegram.ext import CommandHandler, Updater

from . import callbacks


def main():
    """The main function, which is executed when you type ``privilegebot`` or ``python -m privilegebot``."""
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

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
