from src.data_scraping import main as data_scrapper

if __name__ == "__main__":
  import asyncio
  asyncio.run(data_scrapper())
