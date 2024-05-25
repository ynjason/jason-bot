import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class WwConfigs(commands.Cog, name="wwconfigs"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_group(
        name="wwconfigs",
        description="Manage wwconfigs on a server.",
    )
    @commands.has_permissions(manage_messages=True)
    async def wwconfigs(self, context: Context) -> None:
        """
        Manage users on a server.

        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.\n\n**Subcommands:**\n`add` - Add a wwConfig to the server.\n`remove` - Remove a wwConfig from the server.\n`list` - List all wwConfig of the server.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @wwconfigs.command(
        name="add",
        description="Adds a wwConfig to the server.",
    )
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        card_pool_id="cardPoolId",
        player_id="playerId",
        record_id="recordId",
        server_id="serverId"
    )
    async def wwconfigs_add(
        self, context: Context, card_pool_id: str, player_id: str, record_id: str, server_id: str
    ) -> None:
        await self.bot.database.add_config(
            context.author.id, 
            card_pool_id,
            player_id,
            record_id,
            server_id,
        )
        embed = discord.Embed(
            description=f"**{context.author}** ww config was created",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @wwconfigs.command(
        name="remove",
        description="Removes a wwConfig from the server.",
    )
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        user="The user that should be removed for.",
    )
    async def wwconfigs_remove(
        self, context: Context, user: discord.User
    ) -> None:
        total = await self.bot.database.remove_config(user.id)
        embed = discord.Embed(
            description=f"I've removed the ww config for {user}",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @wwconfigs.command(
        name="list",
        description="Shows the ww config of a user in the server.",
    )
    @commands.has_permissions(manage_messages=True)
    async def config_list(self, context: Context) -> None:
        config_list = await self.bot.database.get_configs(context.author.id)
        embed = discord.Embed(title=f"ww configs of {context.author}", color=0xBEBEFE)
        description = ""
        if len(config_list) == 0:
            description = "This user has no configs."
        else:
            for config in config_list:
                description += f"• {config}\n"
        embed.description = description
        await context.send(embed=embed)



async def setup(bot) -> None:
    await bot.add_cog(WwConfigs(bot))
