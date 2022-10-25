from telethon import TelegramClient, events, types
from config import api_id, api_hash, replies
import logging
import random

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING) #not sure if I need this, but API guide said I do

client = TelegramClient('anon', api_id, api_hash)
paused = False

async def main():

    await client.send_message('me', 'Started')
    print('Started')

@client.on(events.NewMessage)
async def reply_on(event):

    global paused

    if event.forward is not None: #do not reply to forwarded messages
        return
    
    author = await event.get_sender()

    if not isinstance(author, types.User): #So we don't get error when trying to access User attributes with Channels which doesn't have it
        return

    if author.is_self is True:
        if event.raw_text == 'Упал?': #To check if the thing is running
            await event.reply("Не упал")
        elif event.raw_text == 'Pause':
            paused = True
            await event.reply("Paused")
        elif event.raw_text == 'Resume':
            paused = False
            await event.reply("Resumed")
        return           

    if paused:
        return

    rep_list = replies.get(author.username)
    if rep_list is not None:
        await event.reply(random.choice(rep_list))

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()