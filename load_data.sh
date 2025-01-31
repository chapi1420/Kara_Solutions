
#!/bin/bash

DB_USER="myuser"
DB_NAME="my_project"
DB_HOST="localhost"
CSV_PATH="/home/nahomnadew/Desktop/10x/week7/Kara_Solutions/data/cleaned_telegram_data.csv"

echo "⚡ Loading data into PostgreSQL..."

psql -U $DB_USER -d $DB_NAME -h $DB_HOST -W -c "\COPY telegram_messages(channel_title,channel_username,message_id,message,message_date,media_path,emoji_used,youtube_links) FROM '$CSV_PATH' DELIMITER ',' CSV HEADER;"

echo "✅ Data successfully loaded!"

