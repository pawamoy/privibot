# privibot
This library provides decorators to restrict access to your Telegram bot handlers based on privileges given to users.
The privileges are stored in a database through SQLAlchemy (SQLite, Postgres, etc.).

## Requirements
privibot requires Python 3.6 or above.

<details>
<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.6
pyenv install 3.6.8

# make it available globally
pyenv global system 3.6.8
```
</details>

## Installation
With `pip`:
```bash
python3.6 -m pip install privibot
```

With [`pipx`](https://github.com/cs01/pipx):
```bash
python3.6 -m pip install --user pipx

pipx install --python python3.6 privibot
```


## Usage
To restrict access to a handler, decorate your callback functions like following:

```python
from privibot import require_access, require_admin


@require_access
def callback_for_registered_users(update, context):
    pass
  
  
@require_admin
def callback_for_admins_only(update, context):
    pass
```

To use custom privileges, define them like so:

```python
# privileges.py
from privibot import Privilege, Privileges as Ps


class Privileges(Ps):
    MEDIA_MANAGER = Privilege(
        name="media_manager",
        verbose_name="Media Manager",
        description="This privilege allows users to act (accept or reject) on media-related requests.",
    )
    USER_MANAGER = Privilege(
        "user_manager", "User Manager", "This privilege allows users to manage access of other users to the bot."
    )
    TESTER = Privilege("tester", "Tester", "This privilege allows users to test new things.")
```

Now simply use these privileges with the decorator:

```python
from privibot import require_privileges

from .privileges import Privileges


@require_privileges([Privileges.USER_MANAGER])
def callback_for_user_managers_only(update, context):
    pass
```

You can also manually check for privileges like so:

```python
from privibot import User

from .privileges import Privileges


def some_callback(update, context):
    telegram_user = update.effective_user
    db_user = User.get_with_id(telegram_user.id)
    
    if db_user.has_privilege(Privileges.TESTER):
        # do something
    elif db_user.has_privileges([Privileges.MEDIA_MANAGER, Privileges.USER_MANAGER]):
        # do something else
```

Users who do not pass the privilege test will receive a message saying they have been denied access.

### Built-in handlers
This library also provides handlers and their callbacks for the following commands:
- /start
- /help
- /requestAccess
- /myPrivileges
- /grant
- /revoke
