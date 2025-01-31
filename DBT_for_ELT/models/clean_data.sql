WITH raw_data AS (
    SELECT * FROM {{ source('staging', '/home/nahomnadew/Desktop/10x/week7/Kara_Solutions/data/cleaned_telegram_data.csv') }}
)

SELECT DISTINCT
    LOWER(trim(channel_title)) AS channel_title,
    LOWER(trim(channel_username)) AS channel_username,
    COALESCE(message_id, 'Unknown') AS message_id,
    COALESCE(message, 'No Message') AS message,
    CAST(message_date AS DATE) AS cleaned_message_date,
    COALESCE(media_path, 'No Media') AS media_path,
    COALESCE(emoji_used, 'No Emoji') AS emoji_used,
    COALESCE(youtube_links, 'No Link') AS youtube_links
FROM raw_data
WHERE channel_title IS NOT NULL;
