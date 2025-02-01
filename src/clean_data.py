import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import re
import emoji

# Load environment variables
load_dotenv()

# Database credentials
DB_NAME = os.getenv("POSTGRES_NAME")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

# Read raw CSV data
file_path = "../data/telegram_data.csv"
df = pd.read_csv(file_path)

# Clean & Transform Data
def clean_content(content):
  """Removes special characters, extracts links separately, extracts emojis, and normalizes spaces."""
  content = str(content).strip()
  links = re.findall(r"https?://\S+", content)  # Extract URLs
  text = re.sub(r"https?://\S+", "", content).strip()  # Remove URLs from text
  text = re.sub(r"\s+", " ", text)  # Normalize spaces
  text = ''.join([c for c in text if c not in emoji.EMOJI_DATA])  # Remove emojis from text
  emojis = ''.join([c['emoji'] for c in emoji.emoji_list(content)])  # Extract emojis
  return text, ",".join(links) if links else None, emojis if emojis else None

# Apply transformations
df[["Message", "Links", "Emojis"]] = df["Content"].apply(lambda x: pd.Series(clean_content(x)))
df["Timestamp"] = pd.to_datetime(df["Timestamp"])  # Ensure timestamp format

# Select useful columns
df_cleaned = df[["Sender", "id", "Message", "Links", "Emojis", "Timestamp"]]

# Save cleaned data to a CSV file
cleaned_csv_path = "../data/cleaned_data.csv"
df_cleaned.to_csv(cleaned_csv_path, index=False)
print(f"Cleaned data saved to {cleaned_csv_path}")

# PostgreSQL Connection
conn = psycopg2.connect(
  dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
cursor = conn.cursor()

# Create Table (if not exists)
create_table_query = """
CREATE TABLE IF NOT EXISTS telegram_messages (
  id SERIAL PRIMARY KEY,
  sender TEXT,
  message_id INT UNIQUE,
  content TEXT,
  links TEXT,
  emojis TEXT,
  timestamp TIMESTAMP
);
"""
cursor.execute(create_table_query)
conn.commit()

# Insert Cleaned Data
insert_query = """
INSERT INTO telegram_messages (sender, message_id, content, links, emojis, timestamp)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (message_id) DO NOTHING;
"""
for _, row in df_cleaned.iterrows():
  cursor.execute(insert_query, (row["Sender"], row["id"], row["Message"], row["Links"], row["Emojis"], row["Timestamp"]))

conn.commit()
cursor.close()
conn.close()

print("Data stored successfully in PostgreSQL!")
