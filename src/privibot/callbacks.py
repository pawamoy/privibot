import logging
from textwrap import dedent

from telegram import ParseMode

from .database import User
from .decorators import require_access, require_admin, require_privileges


def start(update, context):
    tg_user = update.effective_user
    logging.info(f"{tg_user.username} ({tg_user.id}) called /start")

    db_user = User.get_with_id(tg_user.id)

    if not db_user:
        text = dedent(
            f"""
            Hi @{tg_user.username},

            Sorry, but you have not been granted access to my commands.
            Please use the command /requestAccess or contact my administrator.
            """
        )
    else:
        text = dedent(
            f"""
            Nice to meet you, @{tg_user.username}!

            I'm the privilege bot!

            Type the command /help to learn how to use my commands!
            """
        )

    context.bot.send_message(chat_id=update.message.chat_id, text=text)


@require_privileges([])
def help(update, context):
    user = update.message.from_user
    logging.info(f"{user.username} ({user.id}) called /help")
    text = dedent(
        """
        /start - To get an introduction.
        /help - To print this help.
        /requestAccess - To request access to my commands.
        /myPrivileges - To show your current permissions.
        /grant - To grant a privilege to a user.
        /revoke - To revoke a privilege from a user.
    """
    )

    context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.MARKDOWN)


@require_access
def my_privileges(update, context):
    user = update.message.from_user
    logging.info(f"{user.username} ({user.id}) called /myPrivileges")
    db_user = User.get_with_id(user.id)

    text = []
    if db_user:
        if db_user.is_admin:
            text.append("You are an administrator: you have full access to all commands.\n")
        privileges = list(db_user.privileges) if db_user else []
        if privileges:
            text.append("\n" + "\n".join(privileges))
        else:
            text.append("You have zero privileges.")
    else:
        text.append("You do not have access to my commands.")

    context.bot.send_message(chat_id=update.message.chat_id, text="".join(text))


def request_access(update, context):
    tg_user = update.effective_user
    logging.info(f"{tg_user.username} ({tg_user.id}) called /requestAccess")

    user = User.get_with_id(tg_user.id)

    if not user:
        User.create(tg_user.id, tg_user.username)
        context.bot.send_message(
            chat_id=update.message.chat_id, text="I received your request. Please wait for feedback."
        )
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id, text=f"I already know you {tg_user.username}! No need to request access!"
        )


@require_admin
def grant(update, context):
    tg_user = update.effective_user
    logging.info(f"{tg_user.username} ({tg_user.id}) called /grant")

    if (not context.args) or len(context.args) != 2:
        context.bot.send_message(chat_id=update.message.chat_id, text="Usage is /grant <ID_OR_USERNAME> <PERMISSION>")
        return

    permission = context.args[1]
    user = User.get(context.args[0])

    if not user:
        try:
            uid = int(context.args[0])
        except ValueError:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="I don't know that user, please ask them to send '/requestAccess' to me.",
            )
            return
        else:
            user = User.create(uid)

    if user.has_perm(permission):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"User {user.username} ({user.uid}) already has permission '{permission}'.",
        )
        return

    user.grant(permission)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Done! User {user.username} ({user.uid}) now has permission '{permission}'.",
    )

    if update.effective_user.id != user.uid:
        context.bot.send_message(
            chat_id=user.uid,
            text=f"Hi! You've been granted the permission '{permission}' "
            f"just now by {update.effective_user.username} on "
            f"the bot called '{context.bot.username}'. "
            f"If you don't know what this means, just ignore this message!",
        )


@require_admin
def revoke(update, context):
    if not context.args or len(context.args) != 2:
        context.bot.send_message(chat_id=update.message.chat_id, text="Usage is /revoke <ID_OR_USERNAME> <PERMISSION>")
        return

    permission = context.args[1]
    user = User.get(context.args[0])

    if not user:
        try:
            uid = int(context.args[0])
        except ValueError:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text="I don't know that user, please ask them to send '/requestAccess' to me.",
            )
            return
        else:
            user = User.create(uid)

    if not user.has_perm(permission):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"User {user.username} ({user.uid}) does not have permission '{permission}'.",
        )
        return

    user.revoke(permission)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Done! User {user.username} ({user.uid}) just lost permission '{permission}'.",
    )

    if update.effective_user.id != user.uid:
        context.bot.send_message(
            chat_id=user.uid,
            text=f"Hi! You've been revoked the permission '{permission}' "
            f"just now by {update.effective_user.username} on "
            f"the bot called '{context.bot.username}'. "
            f"If you don't know what this means, just ignore this message!",
        )
