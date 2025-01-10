import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} Befehle.")
    except Exception as e:
        print(f"Fehler beim Synchronisieren: {e}")


def create_embed(title: str, description: str, color: discord.Color, interaction: discord.Interaction) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.now()
    )
    embed.set_footer(text=f"Ausgeführt von: {interaction.user}", icon_url=interaction.user.avatar.url)
    return embed


@bot.tree.command(name="ban", description="Bannt einen Benutzer.")
@app_commands.describe(member="Der zu bannende Benutzer", reason="Grund für den Bann")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund angegeben"):
    try:
        await member.ban(reason=reason)
        embed = create_embed(
            title="🔨 Ban erfolgreich",
            description=f"**{member.mention} wurde gebannt.**\nGrund: {reason}",
            color=discord.Color.red(),
            interaction=interaction
        )
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Keine Berechtigung zum Bannen.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Fehler: {e}", ephemeral=True)


@bot.tree.command(name="unban", description="Entbannt einen Benutzer.")
@app_commands.describe(user_id="Die User-ID des zu entbannenden Benutzers")
async def unban(interaction: discord.Interaction, user_id: str):
    try:
        user = await bot.fetch_user(user_id)
        await interaction.guild.unban(user)
        embed = create_embed(
            title="🕊️ Benutzer entbannt",
            description=f"**{user} wurde erfolgreich entbannt.**",
            color=discord.Color.green(),
            interaction=interaction
        )
        await interaction.response.send_message(embed=embed)
    except discord.NotFound:
        await interaction.response.send_message("❌ Benutzer nicht gefunden oder nicht gebannt.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Keine Berechtigung zum Entbannen.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Fehler: {e}", ephemeral=True)


@bot.tree.command(name="kick", description="Kickt einen Benutzer.")
@app_commands.describe(member="Der zu kickende Benutzer", reason="Grund für den Kick")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Kein Grund angegeben"):
    try:
        await member.kick(reason=reason)
        embed = create_embed(
            title="👢 Kick erfolgreich",
            description=f"**{member.mention} wurde gekickt.**\nGrund: {reason}",
            color=discord.Color.orange(),
            interaction=interaction
        )
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Keine Berechtigung zum Kicken.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Fehler: {e}", ephemeral=True)


@bot.tree.command(name="timeout", description="Setzt einen Benutzer in Timeout.")
@app_commands.describe(member="Der Benutzer", duration="Timeout-Dauer in Sekunden")
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int):
    try:
        timeout_until = discord.utils.utcnow() + timedelta(seconds=duration)
        await member.edit(timed_out_until=timeout_until)
        embed = create_embed(
            title="⏱️ Timeout gesetzt",
            description=f"**{member.mention} wurde für {duration} Sekunden in Timeout gesetzt.**",
            color=discord.Color.blue(),
            interaction=interaction
        )
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ Keine Berechtigung für Timeout.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Fehler: {e}", ephemeral=True)


@bot.tree.command(name="removetimeout", description="Entfernt den Timeout eines Benutzers.")
@app_commands.describe(member="Der Benutzer")
async def removetimeout(interaction: discord.Interaction, member: discord.Member):
    try:
        await member.edit(timed_out_until=None)
        embed = create_embed(
            title="🔓 Timeout entfernt",
            description=f"**Timeout von {member.mention} wurde entfernt.**",
            color=discord.Color.green(),
            interaction=interaction
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"❌ Fehler: {e}", ephemeral=True)


@bot.tree.command(name="clear", description="Löscht Nachrichten.")
@app_commands.describe(amount="Anzahl der zu löschenden Nachrichten")
async def clear(interaction: discord.Interaction, amount: int):
    try:
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        embed = create_embed(
            title="🗑️ Nachrichten gelöscht",
            description=f"**{len(deleted)} Nachrichten wurden gelöscht.**",
            color=discord.Color.purple(),
            interaction=interaction
        )
        await interaction.channel.send(embed=embed)
    except discord.Forbidden:
        await interaction.followup.send("❌ Keine Berechtigung zum Löschen von Nachrichten.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Fehler: {e}", ephemeral=True)


bot.run("DEIN TOKEN")
