import os
import csv
import logging
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

# Set up logging
logging.basicConfig(filename='scraping.log', level=logging.INFO, 
          format='%(asctime)s - %(levelname)s - %(message)s')

async def scrape_channel(client, channel_username, writer):
    entity = await client.get_entity(channel_username)
    async for message in client.iter_messages(entity):
        writer.writerow([channel_username, message.id, message.message, message.date])
        logging.info(f"Scraped message {message.id} from {channel_username}")
        if isinstance(message.media, MessageMediaPhoto):
            if channel_username in ['https://t.me/CheMed123', 'https://t.me/lobelia4cosmetics']:
                photo = message.media.photo
                if photo:
                    sanitized_channel_username = channel_username.replace('https://t.me/', '')
                    file_path = f"data/images/{sanitized_channel_username}_{message.id}.jpg"
                    await client.download_media(message.media, file_path)
                    logging.info(f"Downloaded image {file_path} from {channel_username}")

async def main():
    client = TelegramClient('user_session', api_id, api_hash)
    await client.start(phone=phone_number)
    async with client:
        os.makedirs('data/images', exist_ok=True)
        with open('data/telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Sender', 'id', 'Content', 'Timestamp'])

            channels = [
                'https://t.me/DoctorsET',
                'https://t.me/CheMed123',
                'https://t.me/lobelia4cosmetics',
                'https://t.me/yetenaweg',
                'https://t.me/EAHCI',
            ]

            for channel in channels:
                await scrape_channel(client, channel, writer)
                logging.info(f"Completed scraping data from {channel}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())