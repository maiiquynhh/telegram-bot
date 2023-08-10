
import asyncio
import os
import concurrent.futures
import multiprocessing
from telethon import TelegramClient, events, utils
from minio import Minio
import io
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SAVE_DIRECTORY = os.getenv("SAVE_DIRECTORY")

executor = concurrent.futures.ThreadPoolExecutor()

client = TelegramClient("session_name", API_ID, API_HASH)
client.start(bot_token=TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    await event.respond("Bot is running!")

def download_file(file):
    file_path = client.loop.run_in_executor(executor, client.download_media, file)
    return file_path

async def download_and_save_file(event, save_directory):
    try:
        file = event.message
        file_name = file.document.attributes[0].file_name
        file_path = await download_file(file)
        
        # Ensure the file_path is awaited and get its result
        file_path = await file_path
        
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        
        new_file_path = os.path.join(save_directory, file_name)
        
        if os.path.exists(new_file_path):
            existing_file_size = os.path.getsize(new_file_path)
            new_file_size = os.path.getsize(file_path)
            
            if existing_file_size == new_file_size:
                await event.respond(f"File {file_name} already exists with the same size in the destination directory! : {new_file_path}")
                os.remove(file_path)
                return
            else:
                # Append the file size to the new file name
                file_name, file_extension = os.path.splitext(file_name)
                new_file_name = f"{file_name}-{new_file_size}{file_extension}"
                new_file_path = os.path.join(save_directory, new_file_name)
        
        os.rename(file_path, new_file_path)  # Move the file to the desired directory
        await event.respond(f"Downloaded and saved: {file_name}: {new_file_path}")
    except Exception as e:
        await event.respond(f"Error processing file {file_name}: {e}")

# Register the handler for incoming messages
client.add_event_handler(lambda event: download_and_save_file(event, SAVE_DIRECTORY), events.NewMessage(
    func=lambda e: e.media and (e.document.mime_type == "application/zip" or e.document.mime_type == "application/vnd.rar" or e.document.mime_type == "application/x-7z-compressed")
))
# def is_supported_media(event):
#     return event.media and (event.document.mime_type == "application/zip" or event.document.mime_type == "application/vnd.rar")

# # Register the event handler using the decorator
# @events.register(events.NewMessage(func=is_supported_media))
# async def handle_supported_media(event):
#     await download_and_save_file(event, SAVE_DIRECTORY)
    
def main():
    with client:
        # Start the client event loop
        client.run_until_disconnected()

if __name__ == "__main__":
    main()
