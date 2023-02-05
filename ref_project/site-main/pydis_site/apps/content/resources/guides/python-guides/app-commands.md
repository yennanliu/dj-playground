---
title: Discord.py 2.0 changes
description: Changes and new features in version 2.0 of discord.py
---

Upon the return of the most popular discord API wrapper library for Python, `discord.py`, while catching on to the latest features of the discord API, there have been numerous changes with additions of features to the library. Additions to the library include support for Buttons, Select Menus, Forms (AKA Modals), Slash Commands (AKA Application Commands) and a bunch more handy features! All the changes can be found [here](https://discordpy.readthedocs.io/en/latest/migrating.html). Original discord.py Gist regarding resumption can be found [here](https://gist.github.com/Rapptz/c4324f17a80c94776832430007ad40e6).


# Install the latest version of discord.py

Before you can make use of any of the new 2.0 features, you need to install the latest version of discord.py. Make sure that the version is 2.0 or above!
Also, make sure to uninstall any third party libraries intended to add slash-command support to pre-2.0 discord.py, as they are no longer necessary and will likely cause issues.

The latest and most up-to-date stable discord.py version can be installed using `pip install -U discord.py`.

**Before migrating to discord.py 2.0, make sure you read the migration guide [here](https://discordpy.readthedocs.io/en/latest/migrating.html) as there are lots of breaking changes.**.
{: .notification .is-warning }

# What are Slash Commands?

Slash Commands are an exciting new way to build and interact with bots on Discord. As soon as you type "/", you can easily see all the commands a bot has. It also comes with autocomplete, validation and error handling, which will all help users of your bot get the command right the first time.

# Basic structure for discord.py Slash Commands!

### Note that Slash Commands in discord.py are also referred to as **Application Commmands** and **App Commands** and every *interaction* is a *webhook*.
Slash commands in discord.py are held by a container, [CommandTree](https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=commandtree#discord.app_commands.CommandTree). A command tree is required to create Slash Commands in discord.py. This command tree provides a `command` method which decorates an asynchronous function indicating to discord.py that the decorated function is intended to be a slash command. This asynchronous function expects a default argument which acts as the interaction which took place that invoked the slash command. This default argument is an instance of the **Interaction** class from discord.py. Further up, the command logic takes over the behaviour of the slash command.

# Fundamentals for this Gist!

One new feature added in discord.py v2 is `setup_hook`. `setup_hook` is a special asynchronous method of the Client and Bot classes which can be overwritten to perform numerous tasks. This method is safe to use as it is always triggered before any events are dispatched, i.e. this method is triggered before the *IDENTIFY* payload is sent to the discord gateway.
Note that methods of the Bot class such as `change_presence` will not work in setup_hook as the current application does not have an active connection to the gateway at this point.
A full list of commands you can't use in setup_hook can be found [here](https://discord.com/developers/docs/topics/gateway-events#send-events).

__**THE FOLLOWING ARE EXAMPLES OF HOW A `SETUP_HOOK` FUNCTION CAN BE DEFINED**__

Note that the default intents are defined [here](https://discordpy.readthedocs.io/en/stable/api.html?highlight=discord%20intents%20default#discord.Intents.default) to have all intents enabled except presences, members, and message_content.

```python
import discord

# You can create the setup_hook directly in the class definition

class SlashClient(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())

    async def setup_hook(self) -> None:
        ...

# Or add it to the client after creating it

client = discord.Client(intents=discord.Intents.default())
async def my_setup_hook() -> None:
    ...

client.setup_hook = my_setup_hook
```

# Basic Slash Command application using discord.py.

#### The `CommandTree` class resides within the `app_commands` of the discord.py package.

## Slash Command Application with a Client

```python
import discord

class SlashClient(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=discord.Object(id=12345678900987654))
        await self.tree.sync()

client = SlashClient()

@client.tree.command(name="ping", description="...")
async def _ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("pong")

client.run("token")
```


__**EXPLANATION**__

- `import discord` imports the **discord.py** package.
- `class SlashClient(discord.Client)` is a class subclassing **Client**. Though there is no particular reason except readability to subclass the **Client** class, using the `Client.setup_hook = my_func` is equally valid.
- Next up `super().__init__(...)` runs the `__init__` function of the **Client** class, this is equivalent to `discord.Client(...)`. Then, `self.tree = discord.app_commands.CommandTree(self)` creates a CommandTree which acts as the container for slash commands.
- Then in the `setup_hook`, `self.tree.copy_global_to(...)` adds the slash command to the guild of which the ID is provided as a `discord.Object` object. **Essential to creation of commands** Further up, `self.tree.sync()` updates the API with any changes to the Slash Commands.
- Finishing up with the **Client** subclass, we create an instance of the subclassed Client class which here has been named as `SlashClient` with `client = SlashClient()`.
- Then using the `command` method of the `CommandTree` we decorate a function with it as `client.tree` is an instance of `CommandTree` for the current application. The command function takes a default argument as said, which acts as the interaction that took place. Catching up is `await interaction.response.send_message("pong")` which sends back a message to the slash command invoker.
- And the classic old `client.run("token")` is used to connect the client to the discord gateway.
- Note that the `send_message` is a method of the `InteractionResponse` class and `interaction.response` in this case is an instance of the `InteractionResponse` object. The `send_message` method will not function if the response is not sent within 3 seconds of command invocation. We will discuss how to handle this issue later following the Gist.

## Slash Command application with the Bot class

```python
import discord

class SlashBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=".", intents=discord.Intents.default())

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=discord.Object(id=12345678900987654))
        await self.tree.sync()

bot = SlashBot()

@bot.tree.command(name="ping", description="...")
async def _ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("pong")

bot.run("token")
```

The above example shows a basic Slash Commands within discord.py using the Bot class.

__**EXPLANATION**__

Most of the explanation is the same as the prior example that featured `SlashClient` which was a subclass of **discord.Client**. Though some minor changes are discussed below.

- The `SlashBot` class now subclasses `discord.ext.commands.Bot` following the passing in of the required arguments to its `__init__` method.
- `discord.ext.commands.Bot` already consists of an instance of the `CommandTree` class which can be accessed using the `tree` property.

# Slash Commands within a Cog!

A cog is a collection of commands, listeners, and optional state to help group commands together. More information on them can be found on the [Cogs](https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html#ext-commands-cogs) page.

## An Example to using cogs with discord.py for Slash Commands!

```python
import discord
from discord.ext import commands
from discord import app_commands

class MySlashCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="...")
    async def _ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("pong!")

class MySlashBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def setup_hook(self) -> None:
        await self.add_cog(MySlashCog(self))
        await self.tree.copy_global_to(discord.Object(id=123456789098765432))
        await self.tree.sync()

bot = MySlashBot()

bot.run("token")
```

__**EXPLANATION**__

- Firstly, `import discord` imports the **discord.py** package. `from discord import app_commands` imports the `app_commands` module from the **discord.py** root module. `from discord.ext import commands` imports the commands extension.
- Further up, `class MySlashCog(commands.Cog)` is a class subclassing the `Cog` class. You can read more about this [here](https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html#ext-commands-cogs).
- `def __init__(self, bot: commands.Bot): self.bot = bot` is the constructor method of the class that is always run when the class is instantiated and that is why we pass in a **Bot** object whenever we create an instance of the cog class.
- Following up is the `@app_commands.command(name="ping", description="...")` decorator. This decorator basically functions the same as a `bot.tree.command` but since the cog currently does not have a **bot**, the `app_commands.command` decorator is used instead. The next two lines follow the same structure for Slash Commands with **self** added as the first parameter to the function as it is a method of a class.
- The next up lines are mostly the same.
- Talking about the first line inside the `setup_hook` is the `add_cog` method of the **Bot** class. And since **self** acts as the **instance** of the current class, we use **self** to use the `add_cog` method of the **Bot** class as we are inside a subclassed class of the **Bot** class. Then we pass in **self** to the `add_cog` method as the `__init__` function of the **MySlashCog** cog accepts a `Bot` object.
- After that we instantiate the `MySlashBot` class and run the bot using the **run** method which executes our setup_hook function and our commands get loaded and synced. The bot is now ready to use!

# An Example to using groups with discord.py for Slash Commands!

## An example with optional group!

```python
import discord
from discord.ext import commands
from discord import app_commands

class MySlashGroupCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #--------------------------------------------------------
    group = app_commands.Group(name="uwu", description="...")
    #--------------------------------------------------------

    @app_commands.command(name="ping", description="...")
    async def _ping(self, interaction: discord.) -> None:
        await interaction.response.send_message("pong!")

    @group.command(name="command", description="...")
    async def _cmd(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("uwu")

class MySlashBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def setup_hook(self) -> None:
        await self.add_cog(MySlashGroupCog(self))
        await self.tree.copy_global_to(discord.Object(id=123456789098765432))
        await self.tree.sync()

bot = MySlashBot()

bot.run("token")
```

__**EXPLANATION**__
- The only difference used here is `group = app_commands.Group(name="uwu", description="...")` and `group.command`. `app_commands.Group` is used to initiate a group while `group.command` registers a command under a group. For example, the ping command can be run using **/ping** but this is not the case for group commands. They are registered with the format of `group_name command_name`. So here, the **command** command of the **uwu** group would be run using **/uwu command**. Note that only group commands can have a single space between them.

## An example with a **Group** subclass!

```python
import discord
from discord.ext import commands
from discord import app_commands

class MySlashGroup(app_commands.Group, name="uwu"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="ping", description="...")
    async def _ping(self, interaction: discord.) -> None:
        await interaction.response.send_message("pong!")

    @app_commands.command(name="command", description="...")
    async def _cmd(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("uwu")

class MySlashBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def setup_hook(self) -> None:
        await self.add_cog(MySlashGroup(self))
        await self.tree.copy_global_to(discord.Object(id=123456789098765432))
        await self.tree.sync()

bot = MySlashBot()

bot.run("token")
```

__**EXPLANATION**__
- The only difference here too is that the `MySlashGroup` class directly subclasses the **Group** class from discord.app_commands which automatically registers all the methods within the group class to be commands of that specific group. So now, the commands such as `ping` can be run using **/uwu ping** and `command` using **/uwu command**.

# Some common methods and features used for Slash Commands.

### A common function used for Slash Commands is the `describe` function. This is used to add descriptions to the arguments of a slash command. The command function can decorated with this function. It goes by the following syntax as shown below.

```python
from discord.ext import commands
from discord import app_commands
import discord

bot = commands.Bot(command_prefix=".", intents=discord.Intents.default())
#sync the commands

@bot.tree.command(name="echo", description="...")
@app_commands.describe(text="The text to send!", channel="The channel to send the message in!")
async def _echo(interaction: discord.Interaction, text: str, channel: discord.TextChannel=None):
    channel = channel or interaction.channel
    await channel.send(text)
```

### Another common issue that most people come across is the time duration of sending a message with `send_message`. This issue can be tackled by deferring the interaction response using the `defer` method of the `InteractionResponse` class. An example for fixing this issue is shown below.

```python
import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
#sync the commands

@bot.tree.command(name="time", description="...")
async def _time(interaction: discord.Interaction, time_to_wait: int):
    # -------------------------------------------------------------
    await interaction.response.defer(ephemeral=True)
    # -------------------------------------------------------------
    await interaction.edit_original_response(content=f"I will notify you after {time_to_wait} seconds have passed!")
    await asyncio.sleep(time_to_wait)
    await interaction.edit_original_response(content=f"{interaction.user.mention}, {time_to_wait} seconds have already passed!")
```

# Checking for Permissions and Roles!

To add a permissions check to a command, the methods are imported through `discord.app_commands.checks`. To check for a member's permissions, the function can be decorated with the [discord.app_commands.checks.has_permissions](https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=has_permissions#discord.app_commands.checks.has_permissions) method. An example to this as follows.

```py
from discord import app_commands
from discord.ext import commands
import discord

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
#sync commands

@bot.tree.command(name="ping")
@app_commands.checks.has_permissions(manage_messages=True, manage_channels=True) #example permissions
async def _ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")

```

If the check fails, it will raise a `MissingPermissions` error which can be handled within an app commands error handler! We will discuss making an error handler later in the Gist. All the permissions can be found [here](https://discordpy.readthedocs.io/en/latest/api.html?highlight=discord%20permissions#discord.Permissions).

Other methods that you can decorate the commands with are -
- `bot_has_permissions` | This checks if the bot has the required permissions for executing the slash command. This raises a [BotMissingPermissions](https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=app_commands%20checks%20has_role#discord.app_commands.BotMissingPermissions) exception.
- `has_role` | This checks if the slash command user has the required role or not. Only **ONE** role name or role ID can be passed to this. If the name is being passed, make sure to have the exact same name as the role name. This raises a [MissingRole](https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=app_commands%20checks%20has_role#discord.app_commands.MissingRole) exception.
- To pass in several role names or role IDs, `has_any_role` can be used to decorate a command. This raises two exceptions -> [MissingAnyRole](https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=app_commands%20checks%20has_role#discord.app_commands.MissingAnyRole) and [NoPrivateMessage](https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=app_commands%20checks%20has_role#discord.app_commands.NoPrivateMessage)


# Adding cooldowns to Slash Commands!

Slash Commands within discord.py can be applied cooldowns to in order to prevent spamming of the commands. This can be done through the `discord.app_commands.checks.cooldown` method which can be used to decorate a slash command function and register a cooldown to the function. This raises a [CommandOnCooldown](https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=checks%20cooldown#discord.app_commands.CommandOnCooldown) exception if the command is currently on cooldown.
An example is as follows.

```python
from discord.ext import commands
import discord

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="uwu", intents=discord.Intents.all())

    async def setup_hook(self):
        self.tree.copy_global_to(guild=discord.Object(id=12345678909876543))
        await self.tree.sync()


bot = Bot()

@bot.tree.command(name="ping")
# -----------------------------------------
@discord.app_commands.checks.cooldown(1, 30)
# -----------------------------------------
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")

bot.run("token")
```

__**EXPLANATION**__
- The first argument is the number of times this command can be invoked before the cooldown is triggered.
- The second argument it takes is the period of time in which the command can be run the specified number of times.
- The `CommandOnCooldown` exception can be handled using an error handler. We will discuss making an error handler for Slash Commands later in the Gist.


# Handling errors for Slash Commands!

The Slash Commands exceptions can be handled by overwriting the `on_error` method of the `CommandTree`. The error handler takes two arguments. The first argument is the `Interaction` that took place when the error occurred and the second argument is the error that occurred when the Slash Commands was invoked. The error is an instance of [discord.app_commands.AppCommandError](https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=appcommanderror#discord.app_commands.AppCommandError) which is a subclass of [DiscordException](https://discordpy.readthedocs.io/en/latest/api.html?highlight=discordexception#discord.DiscordException).
An example to creating an error handler for Slash Commands is as follows.

```python
from discord.ext import commands
from discord import app_commands
import discord

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
#sync commands

@bot.tree.command(name="ping")
@app_commands.checks.cooldown(1, 30)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")

async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        return await interaction.response.send_message(f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!")
    elif isinstance(error, ...):
        ...
    else:
        raise error

bot.tree.on_error = on_tree_error

bot.run("token")
```

__**EXPLANATION**__

First we create a simple asynchronous function named `on_tree_error` here. To which the first two required arguments are passed, `Interaction` which is named as `interaction` here and `AppCommandError` which is named as `error` here. Then using simple functions and keywords, we make an error handler like above. Here we have used the `isinstance` function which takes in an object and a base class as the second argument, this function returns a bool value. The `raise error` is just for displaying unhandled errors, i.e. the ones which have not been handled manually. If this is **removed**, you will not be able to see any exceptions raised by Slash Commands and makes debugging the code harder.
After creating the error handler function, we set the function as the error handler for the Slash Commands. Here, `bot.tree.on_error = on_tree_error` overwrites the default `on_error` method of the **CommandTree** class with our custom error handler which has been named as `on_tree_error` here.

### Creating an error handler for a specific error!

```python
from discord.ext import commands
from discord import app_commands
import discord

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
#sync commands

@bot.tree.command(name="ping")
@app_commands.checks.cooldown(1, 30)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")

@ping.error
async def ping_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        return await interaction.response.send_message(f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!")
    elif isinstance(error, ...):
        ...
    else:
        raise error

bot.run("token")
```

__**EXPLANATION**__

Here the command name is simply used to access the `error` method to decorate a function which acts as the `on_error` but for a specific command. You should not need to call the `error` method manually.
