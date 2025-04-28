import asyncio
import random
import os
from discord.ext import commands
import discord

# Get user token from environment variable (Replit secret)
token = os.getenv("DISCORD_TOKEN")

prefix = "!"
dmcs = False
target_channel = None
fast_task = None
medium_task = None
long_task = None

client = commands.Bot(command_prefix=prefix, self_bot=True)

# FAST loop (+broadcast and +beg)
async def fast_loop():
    global dmcs, target_channel
    await asyncio.sleep(5)
    while dmcs and target_channel:
        try:
            commands_fast = ["+broadcast", "+beg"]
            random.shuffle(commands_fast)
            for cmd in commands_fast:
                if not dmcs:
                    break
                await target_channel.send(cmd)
                print(f"Sent: {cmd}")
                await asyncio.sleep(random.randint(3, 6))  # small delay between
            wait_time = random.randint(120, 121)  # 2-3 minutes
            print(f"Waiting {wait_time} seconds before next fast cycle.")
            await asyncio.sleep(wait_time)
        except Exception as e:
            print(f"Error in fast loop: {e}")
            await asyncio.sleep(5)

# MEDIUM loop (+harvest, +wolf, +pickaxe, +oilminer, +iron, +navy fish, +bread, +work)
async def medium_loop():
    global dmcs, target_channel
    await asyncio.sleep(10)
    while dmcs and target_channel:
        try:
            commands_medium = ["+harvest", "+wolf", "+pickaxe", "+oilminer", "+iron", "+navy fish", "+bread", "+work"]
            random.shuffle(commands_medium)
            for cmd in commands_medium:
                if not dmcs:
                    break
                await target_channel.send(cmd)
                print(f"Sent: {cmd}")
                await asyncio.sleep(random.randint(4, 7))  # small delay between
            wait_time = random.randint(900, 1020)  # 15-17 minutes
            print(f"Waiting {wait_time} seconds before next medium cycle.")
            await asyncio.sleep(wait_time)
        except Exception as e:
            print(f"Error in medium loop: {e}")
            await asyncio.sleep(5)

# LONG loop (+recruit)
async def long_loop():
    global dmcs, target_channel
    await asyncio.sleep(15)
    while dmcs and target_channel:
        try:
            await target_channel.send("+recruit")
            print("Sent: +recruit")
            wait_time = random.randint(1860, 1980)  # 31-33 minutes
            print(f"Waiting {wait_time} seconds before next recruit.")
            await asyncio.sleep(wait_time)
        except Exception as e:
            print(f"Error in long loop: {e}")
            await asyncio.sleep(5)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("Bot is ready!")

@client.command()
async def start(ctx, channel_id: int):
    global dmcs, target_channel, fast_task, medium_task, long_task

    if dmcs:
        await ctx.message.reply("⚠️ Already running.")
        return

    channel = client.get_channel(channel_id)
    if not channel:
        await ctx.message.reply("❌ Invalid channel ID.")
        return

    dmcs = True
    target_channel = channel
    await ctx.message.reply(f"✅ Started sending commands in {channel.mention}.")

    fast_task = asyncio.create_task(fast_loop())
    medium_task = asyncio.create_task(medium_loop())
    long_task = asyncio.create_task(long_loop())

@client.command()
async def stop(ctx):
    global dmcs, target_channel, fast_task, medium_task, long_task

    if not dmcs:
        await ctx.message.reply("⚠️ Not running.")
        return

    dmcs = False
    target_channel = None

    if fast_task:
        fast_task.cancel()
    if medium_task:
        medium_task.cancel()
    if long_task:
        long_task.cancel()

    await ctx.message.reply("⛔ Stopped sending commands.")

# Auto-restart loop
while True:
    try:
        client.run(token)
    except Exception as e:
        print(f"Bot crashed with error: {e}")
        print("Restarting in 5 seconds...")
        asyncio.run(asyncio.sleep(5))
