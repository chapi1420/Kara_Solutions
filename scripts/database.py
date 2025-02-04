import os
import logging
from sqlalchemy import create_engine, text
import pandas as pd

class DatabaseManager:
    def __init__(self, db_host, db_name, db_user, db_password, db_port=5432, log_dir="../logs"):
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port
        self.engine = None
        
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(f"{log_dir}/database_setup.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def connect(self):
        try:
            database_url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
            self.engine = create_engine(database_url)
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            self.logger.info("✅ Successfully connected to the PostgreSQL database.")
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            raise

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS telegram_messages (
            id SERIAL PRIMARY KEY,
            channel_title TEXT,
            channel_username TEXT,
            message_id BIGINT UNIQUE,
            message TEXT,
            message_date TIMESTAMP,
            media_path TEXT,
            emoji_used TEXT,
            youtube_links TEXT
        );
        """
        try:
            with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
                connection.execute(text(create_table_query))
            self.logger.info("✅ Table 'telegram_messages' created successfully.")
        except Exception as e:
            self.logger.error(f"❌ Error creating table: {e}")
            raise

    def insert_data(self, cleaned_df):
        try:
            cleaned_df["message_date"] = cleaned_df["message_date"].apply(lambda x: None if pd.isna(x) else str(x))
            insert_query = """
            INSERT INTO telegram_messages 
            (channel_title, channel_username, message_id, message, message_date, media_path, emoji_used, youtube_links) 
            VALUES (:channel_title, :channel_username, :message_id, :message, :message_date, :media_path, :emoji_used, :youtube_links)
            ON CONFLICT (message_id) DO NOTHING;
            """
            with self.engine.begin() as connection:
                for _, row in cleaned_df.iterrows():
                    self.logger.info(f"Inserting: {row['message_id']} - {row['message_date']}")
                    connection.execute(
                        text(insert_query),
                        {
                            "channel_title": row["channel_title"],
                            "channel_username": row["channel_username"],
                            "message_id": row["message_id"],
                            "message": row["message"],
                            "message_date": row["message_date"],
                            "media_path": row["media_path"],
                            "emoji_used": row["emoji_used"],
                            "youtube_links": row["youtube_links"]
                        }
                    )
            self.logger.info(f"✅ {len(cleaned_df)} records inserted into PostgreSQL database.")
        except Exception as e:
            self.logger.error(f"❌ Error inserting data: {e}")
            raise
