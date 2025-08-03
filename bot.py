import os
from dotenv import load_dotenv

load_dotenv()  # This loads environment variables from your .env file

import discord
from discord import app_commands
import random
import asyncio

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Your Discord bot token here
TOKEN = os.getenv('TOKEN')
# Your guild/server ID here
GUILD_ID = 1386289738419535882  # replace with int, e.g. 1234567890
# Role ID allowed to use spin command
ALLOWED_ROLE_ID = 1386674622275125421  # replace with int

# Define Market Wheel prizes (period '.' means rigged prize)
market_wheel = [
    "200 Robux", "600 Robux", "1000 Robux", "1850 Robux",
    "Silver Rank", "Platinum Rank", "Emerald Rank", "Diamond Rank",
    "250K Coins", "500K Coins", "850K Coins", "1,25M Coins",
    "2,5M Coins", "500M Coins."
]

def get_rigged_prize(prizes):
    for prize in prizes:
        if '.' in prize:
            return prize
    return None

@tree.command(name="spin-wheel", description="Spin the Market Wheel!", guild=discord.Object(id=GUILD_ID))
async def spin_wheel(interaction: discord.Interaction):
    user_role_ids = [role.id for role in interaction.user.roles]
    if ALLOWED_ROLE_ID not in user_role_ids:
        await interaction.response.send_message("⛔ You are not allowed to spin the Market Wheel.", ephemeral=True)
        return

    rigged = get_rigged_prize(market_wheel)
    final_prize = rigged if rigged else random.choice(market_wheel)
    final_prize_clean = final_prize.replace('.', '')

    # Defer the response to buy more time (shows "Bot is thinking...")
    await interaction.response.defer(ephemeral=False)
    message = await interaction.original_response()

    spins = market_wheel * 2
    random.shuffle(spins)
    spins.append(final_prize)

    total_spin_time = 7  # seconds
    base_delay = total_spin_time / len(spins)  # distribute delay evenly

    delay = base_delay
    for i, prize in enumerate(spins):
        # Show spinning message with current prize
        if i < len(spins) - 1:
            await message.edit(content=f"🎯 Spinning... {prize.replace('.', '')}")
        else:
            # Last one: show the winning message
            await message.edit(content=f"🎉 You won: **{final_prize_clean}**")
        await asyncio.sleep(delay)
        # Slow down near the end (last 6 spins)
        if i > len(spins) - 7:
            delay *= 1.3  # increase delay gradually



@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await tree.sync(guild=discord.Object(id=GUILD_ID))

client.run(TOKEN)
