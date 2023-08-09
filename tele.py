
import asyncio
import os
import concurrent.futures
import multiprocessing
from telethon import TelegramClient, events, utils
from minio import Minio
import io

import logging
logging.basicConfig(level=logging.DEBUG)

TOKEN = "BOT_TOKEN" 

MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "MINIO_ACCESS_KEY"
MINIO_SECRET_KEY = "MINIO_SECRET_KEY"
MINIO_BUCKET_NAME = "downloader-bot"
API_ID = 1234567 
API_HASH = "API_HASH"

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

# Telethon configurations
API_ID = 1234567 
API_HASH = "API_HASH"

executor = concurrent.futures.ThreadPoolExecutor()

# Initialize the Telethon client
client = TelegramClient("session_name", API_ID, API_HASH)
client.start(bot_token=TOKEN)

# Process the /start command
@client.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    await event.respond("Bot is running!")

def file_exists_in_minio(file_data):
    try:
        objects = minio_client.list_objects(bucket_name=MINIO_BUCKET_NAME)
        for obj in objects:
            existing_data = minio_client.get_object(bucket_name=MINIO_BUCKET_NAME, object_name=obj.object_name)
            existing_data = io.BytesIO(existing_data.read())
            if existing_data.getvalue() == file_data.getvalue():
                return True
    except Exception as e:
        return False
    return False

def download_file(file):
    file_path = client.loop.run_in_executor(executor, client.download_media, file)
    return file_path

# Function to download file and upload to MinIO
async def download_and_upload_file(bot, event, file):
    try:
        file_name = file.document.attributes[0].file_name
        # file_path = await client.download_media(file)  # Get the file path
        file_path = await download_file(file)
        
        # Ensure the file_path is awaited and get its result
        file_path = await file_path
        
        with open(file_path, 'rb') as file_stream:
            file_data = io.BytesIO(file_stream.read())  # Read file contents
        file_size = len(file_data.getvalue())
        unique_file_name = f"{file_name}-{file_size}"

        # Check if the file with the same content exists in MinIO
        if file_exists_in_minio(file_data):
            await event.respond(f"File {file_name} already exists in MinIO!")
            return

        # Upload the file to MinIO
        minio_client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=unique_file_name,
            data=file_data,
            length=len(file_data.getvalue()),
        )
        await event.respond(f"Uploaded: {file_name} to MinIO successfully!")
        os.remove(file_path)
    except Exception as e:
        await event.respond(f"Error processing file {file_name}: {e}")

# Handle incoming messages
@client.on(events.NewMessage)
async def handle_message(event):
    if event.media and (event.document.mime_type == "application/zip" or event.document.mime_type == "application/vnd.rar"):
        try:
            await download_and_upload_file(client, event, event.message)
        except Exception as e:
            await event.respond(f"Error handling file: {e}")

def main():
    with client:
        # Start the client event loop
        client.run_until_disconnected()

if __name__ == "__main__":
    main()

