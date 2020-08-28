# lmaobot.py

import os
from _datetime import datetime
from asyncio import sleep

import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord import Attachment, Message, MessageType, mentions
from lmaobot_util import chunk_string, parse_replay, fancy_chunk_string
import io
load_dotenv()
TOKEN = os.getenv('TOKEN')

lmaobot = commands.Bot(command_prefix='?.')

@lmaobot.event
async def on_ready():
    print('lmaobot is ready.\n')


@lmaobot.event
async def on_message(msg: discord.Message):

    if msg.author == lmaobot.user:
        return
    elif msg.channel.name == "replays-channel" or msg.channel.name == "bm_screenshots" or msg.channel.name == "sc2-logs":
        if len(msg.attachments) > 0:
            for attachment in msg.attachments:
                print(attachment.filename)
                file_name = attachment.filename
                if file_name[file_name.__len__() - 10:] == '.SC2Replay':
                    # replay_filename = f'{attachment.filename}-{attachment.id}.SC2Replay'
                    buffer = io.BytesIO()
                    await attachment.save(
                        buffer,
                        seek_begin=True,
                        use_cached=False
                    )
                    replay_chat_text = parse_replay(buffer)
                    if replay_chat_text.__len__() > 2000:
                        chunked_chat_substring = fancy_chunk_string(replay_chat_text)
                        for string in chunked_chat_substring:
                            mess = await msg.channel.send(string)
                            print(mess)
                    else:
                        mess = await msg.channel.send(replay_chat_text)
                        print(mess)

def print_msg(msg):
    print(f'{msg.channel.name} {msg.author.name}: {msg.content}')


lmaobot.run(TOKEN)
