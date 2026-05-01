"""
Midjourney Prompt Bot
Sends your prompt to Midjourney on Discord and saves the generated image.

Install:
    pip install discord.py-self requests

Setup:
    1. DISCORD_TOKEN  → Discord user token (F12 on discord.com → Network → any request → Authorization header)
    2. CHANNEL_ID     → Channel where Midjourney bot is active (Right-click → Copy ID, needs Developer Mode on)
    3. Run: python mj_bot.py
    4. Type your prompt when asked → image saved to midjourney_output/
"""

import os
import re
import time
import asyncio
import requests
from pathlib import Path
from datetime import datetime

import discord  # pip install discord.py-self

# ============================================================
#  CONFIG
# ============================================================
DISCORD_TOKEN = "YOUR_USER_TOKEN_HERE"   # Your Discord account token
CHANNEL_ID    = 123456789012345678        # Channel ID (integer, no quotes)
OUTPUT_FOLDER = "midjourney_output"       # Folder to save images
TIMEOUT       = 300                       # Seconds to wait for Midjourney (5 min)
# ============================================================

Path(OUTPUT_FOLDER).mkdir(exist_ok=True)
client = discord.Client()
_prompt_sent    = False
_prompt_text    = ""
_waiting        = False
_done_event     = asyncio.Event()


def save_image(url: str, prompt: str) -> str:
    slug  = re.sub(r"[^\w\s-]", "", prompt[:40]).strip().replace(" ", "_")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext   = url.split("?")[0].rsplit(".", 1)[-1] or "png"
    name  = f"{stamp}_{slug}.{ext}"
    path  = Path(OUTPUT_FOLDER) / name

    print(f"\n  Downloading image → {name}")
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    with open(path, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)
    return str(path.resolve())


def is_mj_result(msg: discord.Message) -> bool:
    """True if this looks like a finished Midjourney grid (not 'Waiting…' or progress)."""
    if msg.author.id != 936929561302675456:   # Midjourney Bot ID
        return False
    if not msg.attachments:
        return False
    # Progress messages contain a % — skip them
    if re.search(r"\(\d+%\)", msg.content or ""):
        return False
    return True


@client.event
async def on_ready():
    global _waiting
    print(f"  Logged in as: {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("  ERROR: Channel not found. Check CHANNEL_ID.")
        await client.close()
        return

    print(f"  Channel: #{channel.name}")
    print(f"\n  Sending prompt to Midjourney...")
    await channel.send(f"/imagine prompt: {_prompt_text}")
    print(f"  Prompt sent. Waiting for image (up to {TIMEOUT}s)...\n")
    _waiting = True

    # Timeout watcher
    async def timeout_watcher():
        await asyncio.sleep(TIMEOUT)
        if not _done_event.is_set():
            print("\n  TIMEOUT: Midjourney did not respond in time.")
            _done_event.set()
            await client.close()

    asyncio.create_task(timeout_watcher())


@client.event
async def on_message(msg: discord.Message):
    global _waiting
    if not _waiting:
        return
    if msg.channel.id != CHANNEL_ID:
        return

    # Show progress updates
    if msg.author.id == 936929561302675456 and msg.content:
        if re.search(r"\(\d+%\)", msg.content):
            pct = re.search(r"\((\d+)%\)", msg.content).group(1)
            print(f"  Midjourney progress: {pct}%", end="\r")

    if is_mj_result(msg):
        url  = msg.attachments[0].url
        path = save_image(url, _prompt_text)
        print(f"\n  Image saved → {path}")
        _done_event.set()
        await client.close()


async def run(prompt: str):
    global _prompt_text
    _prompt_text = prompt
    await client.start(DISCORD_TOKEN)


def main():
    if DISCORD_TOKEN == "YOUR_USER_TOKEN_HERE":
        print("ERROR: Set your DISCORD_TOKEN in the script.")
        print("\nHow to get it:")
        print("  1. Open discord.com/app in Chrome")
        print("  2. Press F12 → Network tab")
        print("  3. Reload → click any request → Headers")
        print("  4. Find 'authorization' → copy that value")
        return

    print("=" * 50)
    print("  Midjourney Prompt Bot")
    print("=" * 50)
    prompt = input("\nEnter your prompt: ").strip()
    if not prompt:
        print("No prompt entered.")
        return

    asyncio.run(run(prompt))


if __name__ == "__main__":
    main()
